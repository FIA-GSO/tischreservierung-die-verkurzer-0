from __main__ import app
from flask import request
from datetime import datetime


def parse_date_string(date_string, date_format):
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        return None


@app.route('/getTables', methods=['GET'])
def get_tables():
    date_format = "%Y-%m-%d-%H:%M:%S"
    args = request.args
    fromTime = args.get('from')
    toTime = args.get('to')
    fromTime = "2023-10-17-15:30:00"

    if fromTime:
        parsed_date = parse_date_string(fromTime, date_format)
        if parsed_date:
            print("Parsed date:", parsed_date)
        else:
            print("Fehler beim Parsen des Datums.")
    if toTime:
        parsed_date = parse_date_string(fromTime, date_format)
        if parsed_date:
            print("Parsed date:", parsed_date)
        else:
            print("Fehler beim Parsen des Datums.")