import os

import flask
from flask import request  # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify  # übersetzt python-dicts in json
from flask import Response
from datetime import datetime, timedelta

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
        results = query_db(
            "SELECT tischnummer AS Tisch FROM reservierungen WHERE reservierungen.zeitpunkt not like '" + datify(
                date_time) + "'")
        return jsonify(results)
    else:
        return Response(' ? time= format: ' + date_format + ' muss definiert sein')


date_format = "%Y-%m-%d--%H:%M:%S"
date_format_db = "%Y-%m-%d %H:%M:%S"


@app.route('/getReservierungen', methods=['GET'])
def get_reservierungen():
    results = query_db("SELECT * FROM reservierungen")
    return jsonify(results)


def is_colliding(start_date_time, end_date_time, reservierung):
    start_time = datetime.strptime(start_date_time, date_format)
    end_time = datetime.strptime(end_date_time, date_format)
    res_start = datetime.strptime(reservierung.get("zeitpunkt"), date_format_db)
    res_end = res_start + timedelta(minutes=reservierung.get('dauerMin'))
    return not (start_time < res_start and start_time < res_end and end_time < res_start and end_time < res_end) or (start_time > res_start and start_time > res_end and end_time > res_start and end_time > res_end)

@app.route('/getFreeTables', methods=['GET'])
def get_free_tables():
    args = request.args
    start_date_time = args.get('start_time')
    end_date_time = args.get('end_time')

    if start_date_time and end_date_time:
        # Error handling bei inkorektem Datum/Zeit Format
        # get allReservierung
        wertespeicherReservierteTischnummern = []
        allReservierung = query_db("SELECT * FROM reservierungen")
        # for: allReservierung iterieren
        for reservierung in allReservierung:
            # if: vergleichen reservierungszeitraum mit dem gegebenen; kollidiert oder kollidiert nicht
            if is_colliding(start_date_time, end_date_time, reservierung):
                # wenn es nicht kollidiert nichts machen
                # wenn kollidiert: speicher tischnummer
                wertespeicherReservierteTischnummern.append(reservierung.get('tischnummer'))

        # get allTische
        allTische = list(map(lambda tisch: tisch.get('tischnummer'), query_db("SELECT tischnummer FROM tische")))
        def isNotReserved(tischnummer):
            return not tischnummer in wertespeicherReservierteTischnummern

        # freienTische = ziehe alle kollidierenden Tischnummern von allTische ab
        freiTische = list(filter(isNotReserved, allTische))
        # return freienTische
        return (jsonify(freiTische))
    else:
        return Response('Error: Jeweils Start und End Zeit müssen gegeben sein')

app.run()
