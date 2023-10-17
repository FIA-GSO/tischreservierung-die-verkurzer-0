import os

import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
from flask import Response
from datetime import datetime
from db import init_db

app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message
init_db()


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


def parse_date_string(date_string, date_format):
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        return None


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/getTables', methods=['GET'])
def get_tables():
    date_format = "%Y-%m-%d-%H:%M:%S"
    args = request.args
    fromTime = args.get('from')
    toTime = args.get('to')
    if fromTime and toTime:
        parsed_date1 = parse_date_string(fromTime, date_format)
        parsed_date2 = parse_date_string(toTime, date_format)
        if parsed_date1 and parsed_date2:
            formatted_date1 = parsed_date1.strftime(date_format)
            formatted_date2 = parsed_date2.strftime(date_format)
            return Response('from: ' + formatted_date1 + ' to: ' + formatted_date2)
        else:
            return Response("Fehler beim Parsen des Datums.")
    else:
        return Response(' ? from="%Y-%m-%d-%H:%M:%S & to="%Y-%m-%d-%H:%M:%S müssen definiert sein')


app.run()