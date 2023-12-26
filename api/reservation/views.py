
from flask import request, jsonify, Response

from api.reservation import crud
from api.reservation.models import Reservation


def init_reservation_routes(app):

    @app.route('/reservations', methods=['GET', 'POST', 'PATCH'])
    def handle_reservations():
        if request.method == 'GET':
            return get_reservations()
        elif request.method == 'POST':
            return add_reservation()
        return cancel_reservation()

    def get_reservations():
        results = crud.read_all_reservations()
        return jsonify(results)

    def add_reservation():
        try:
            reservation = Reservation(**request.json)
            crud.create_reservation(reservation)
            return Response('New reservation added', status=201)
        except Exception as e:
            return Response(str(e), status=400)

    def cancel_reservation():
        reservation_number = request.json.get('reservation_number')
        crud.update_reservation_cancel(reservation_number, True)
        return Response('Reservation canceled', status=200)
