from datetime import datetime

from flask import request, jsonify, Response
from pydantic import BaseModel, field_validator

from api.db import query_db
date_format = "%Y-%m-%d %H:%M:%S"


def init_reservation_routes(app):

    @app.route('/reservations', methods=['GET', 'POST', 'PATCH'])
    def handle_reservations():
        if request.method == 'GET':
            return get_reservations()
        elif request.method == 'POST':
            return add_reservation()
        return cancel_reservation()  # This is PATCH

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
            )  # Assuming new reservations are not cancelled

            return Response('New reservation added', status=201)
        except Exception as e:
            return Response(str(e), status=400)

    def cancel_reservation():
        reservation_number = request.json.get('reservation_number')
        query_db("UPDATE reservierungen SET storniert ='True' WHERE reservierungsnummer =?", (reservation_number,),)
        return Response('Reservation canceled', status=200)
