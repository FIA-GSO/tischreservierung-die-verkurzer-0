db_date_format = "%Y-%m-%d %H:%M:%S"
request_date_format = "%Y-%m-%d--%H:%M:%S"


def datify(date):
    return date.replace('--', ' ')

