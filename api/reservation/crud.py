from api.db import query_db


def read_all_reservations():
    return query_db("SELECT * FROM reservierungen")


def create_reservation(reservation):
    query_db(
        "INSERT INTO reservierungen (reservierungsnummer, zeitpunkt, dauerMin, tischnummer, pin, storniert) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (reservation.reservation_number, reservation.timestamp,
         reservation.duration_minutes, reservation.table_number, reservation.pin,
         'False'),
    )


def update_reservation_cancel(reservation_number, is_canceled):
    query_db("UPDATE reservierungen SET storniert = ? WHERE reservierungsnummer = ?",
             ('True' if is_canceled else 'False', reservation_number))
