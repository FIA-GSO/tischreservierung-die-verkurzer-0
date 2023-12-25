from datetime import datetime, timedelta

from flask import request, jsonify, Response

from ..db import query_db

date_format = "%Y-%m-%d %H:%M:%S"


def init_table_routes(app):

    def datify(date):
        return date.replace('--', ' ')

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
            return Response('Error: Both start and end times must be provided'), 400

    def is_colliding(start_date_time, end_date_time, reservation):
        start_time = datetime.strptime(start_date_time, date_format)
        end_time = datetime.strptime(end_date_time, date_format)
        res_start = datetime.strptime(reservation.get("zeitpunkt"), date_format)
        res_end = res_start + timedelta(minutes=reservation.get('dauerMin'))
        return not (
                start_time < res_start and start_time < res_end and end_time < res_start and end_time < res_end) or (
                start_time > res_start and start_time > res_end and end_time > res_start and end_time > res_end)
