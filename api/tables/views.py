from datetime import datetime

from flask import request, jsonify, Response

from api.tables import crud
from ..utils.dateformat import datify, request_date_format


def init_table_routes(app):

    @app.route('/tables', methods=['GET'])
    def get_tables():
        results = crud.read_all_tables()
        return jsonify(results)

    @app.route('/tables/free', methods=['GET'])
    def get_free_tables():
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time and end_time:
            try:
                datetime.strptime(start_time, request_date_format)
                datetime.strptime(end_time, request_date_format)
            except ValueError:
                return Response(f"Incorrect date format, should be {request_date_format}"), 400

            db_start_time = datify(start_time)
            db_end_time = datify(end_time)
            free_tables = crud.read_all_free_tables(db_start_time, db_end_time)
            return jsonify(free_tables)
        else:
            return Response('Error: Both start and end times must be provided'), 400
