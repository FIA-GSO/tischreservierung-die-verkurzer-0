from datetime import datetime, timedelta

from api.db import query_db
from api.reservation.crud import read_all_reservations
from api.utils.dateformat import db_date_format


def read_all_tables():
    return query_db("SELECT * FROM tische")


def _is_colliding(start_date_time, end_date_time, reservation):
    start_time = datetime.strptime(start_date_time, db_date_format)
    end_time = datetime.strptime(end_date_time, db_date_format)
    res_start = datetime.strptime(reservation.get("zeitpunkt"), db_date_format)
    res_end = res_start + timedelta(minutes=reservation.get('dauerMin'))
    return not (
            start_time < res_start and start_time < res_end and end_time < res_start and end_time < res_end) or (
            start_time > res_start and start_time > res_end and end_time > res_start and end_time > res_end)


def read_all_free_tables(start_time, end_time):
    all_reservations = read_all_reservations()
    reserved_tables = [
        res['tischnummer'] for res in all_reservations
        if _is_colliding(start_time, end_time, res)
    ]
    all_tables = read_all_tables()
    free_tables = [table['tischnummer'] for table in all_tables if table['tischnummer'] not in reserved_tables]
    return free_tables
