import os
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator

date_format = "%Y-%m-%d--%H:%M:%S"

app = Flask(__name__)
app.config["DEBUG"] = True  # Enables detailed error messages in the browser

from db import init_db, query_db

init_db()


# Configuration for serving the Swagger file
SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our Swagger document
swagger_destination_path = './static/swagger.yaml'



def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


def datify(date):
    return date.replace('--', ' ')


@app.route('/', methods=['GET'])
def metrics():
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/tables', methods=['GET'])
def get_tables():
    args = request.args
    date_time = args.get('time')

    if date_time:
        date_time = date_time.replace('--', ' ')
        results = query_db(
            "SELECT tischnummer AS Tisch FROM reservierungen WHERE reservierungen.zeitpunkt not like '" + datify(
                date_time) + "'")
        return jsonify(results)
    else:
        return Response(f' ? time= format: {date_format} must be defined')


@app.route('/free-tables', methods=['GET'])
def get_free_tables():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if start_time and end_time:
        all_reservations = query_db("SELECT * FROM reservierungen")
        reserved_tables = [
            res['tischnummer'] for res in all_reservations
            if is_colliding(start_time, end_time, res)
        ]
        all_tables = query_db("SELECT tischnummer FROM tische")
        free_tables = [table['tischnummer'] for table in all_tables if table['tischnummer'] not in reserved_tables]
        return jsonify(free_tables)
    else:
        return Response('Error: Both start and end times must be provided')


def is_colliding(start_date_time, end_date_time, reservation):
    start_time = datetime.strptime(start_date_time, date_format)
    end_time = datetime.strptime(end_date_time, date_format)
    res_start = datetime.strptime(reservation.get("zeitpunkt"), date_format)
    res_end = res_start + timedelta(minutes=reservation.get('dauerMin'))
    return not (
            start_time < res_start and start_time < res_end and end_time < res_start and end_time < res_end) or (
            start_time > res_start and start_time > res_end and end_time > res_start and end_time > res_end)


@app.route('/reservations', methods=['GET', 'PUT', 'POST'])
def handle_reservations():
    if request.method == 'GET':
        return get_reservations()
    elif request.method == 'PUT':
        return add_reservation()
    elif request.method == 'POST':  # More fitting would be PATCH but the swagger generation package does not support it
        return cancel_reservation()



def get_reservations():
    results = query_db("SELECT * FROM reservierungen")
    return jsonify(results)


class Reservation(BaseModel):
    table_number: int
    duration_minutes: int
    pin: int
    reservation_number: int
    timestamp: str

    @field_validator('timestamp')
    def valid_timestamp(cls, v):
        try:
            datetime.strptime(v, date_format)
            return v
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD HH:MM:SS")


def add_reservation():
    reservation_details = Reservation(**request.json)
    query_db("INSERT INTO reservierungen (tischnummer, zeitpunkt, ...) VALUES (?, ?, ...)",
             (reservation_details.table_number, ...))
    return Response('New reservation added', status=201)


def cancel_reservation():
    reservation_number = request.json.get('reservation_number')
    query_db("UPDATE reservierungen SET storniert = TRUE WHERE reservierungsnummer = %s", (reservation_number,))
    return Response('Reservation canceled', status=200)


app.run()
