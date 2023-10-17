import os

import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
from flask import Response


app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message
from db import init_db, query_db
init_db()


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


def datify(date):
    return date.replace('--', ' ')


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/getTables', methods=['GET'])
def get_tables():
    date_format = "year-month-day--hour:minute:seconds"
    args = request.args
    date_time = args.get('time')

    if date_time:
            results = query_db("SELECT tischnummer AS Tisch FROM reservierungen WHERE reservierungen.zeitpunkt not like '" + datify(date_time) + "'")
            return jsonify(results)
    else:
        return Response(' ? time= format: ' + date_format + ' muss definiert sein')


@app.route('/getReservierungen', methods=['GET'])
def get_reservierungen():
    results = query_db("SELECT * FROM reservierungen")
    return jsonify(results)


app.run()