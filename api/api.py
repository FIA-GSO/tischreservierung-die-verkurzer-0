import os
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator
from db import init_db, query_db

date_format = "%Y-%m-%d %H:%M:%S"


def init_app(app):
    # Configuration for serving the Swagger file
    SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.yaml'  # Our Swagger document
    swagger_destination_path = './static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Tisch Reservierung"
        }
    )

    # Register blueprint at URL
    # (URL must match the one given to get_swaggerui_blueprint)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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
        results = query_db(
            "SELECT tischnummer AS Tisch ,anzahlPlaetze AS Plaetze FROM tische")
        return jsonify(results)

    @app.route('/tables/free', methods=['GET'])
    def get_free_tables():
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time and end_time:
            all_reservations = query_db("SELECT * FROM reservierungen")
            reserved_tables = [
                res['tischnummer'] for res in all_reservations
                if is_colliding(datify(start_time), datify(end_time), res)
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

    @app.route('/reservations', methods=['GET', 'POST', 'PATCH'])
    def handle_reservations():
        if request.method == 'GET':
            return get_reservations()
        elif request.method == 'POST':
            return add_reservation()
        elif request.method == 'PATCH':
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
        try:
            reservation_details = Reservation(**request.json)
            query_db(
                "INSERT INTO reservierungen (reservierungsnummer, zeitpunkt, dauerMin, tischnummer, pin, storniert) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (reservation_details.reservation_number, reservation_details.timestamp,
                 reservation_details.duration_minutes, reservation_details.table_number, reservation_details.pin,
                 'False'),
                commit=True
            )  # Assuming new reservations are not cancelled

            return Response('New reservation added', status=201)
        except Exception as e:
            return Response(str(e), status=400)

    def cancel_reservation():
        reservation_number = request.json.get('reservation_number')
        query_db("UPDATE reservierungen SET storniert = TRUE WHERE reservierungsnummer = %s", (reservation_number,),
                 commit=True)
        return Response('Reservation canceled', status=200)


def create_app():
    app = Flask(__name__)
    init_app(app)
    init_db(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
