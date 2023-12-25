from flask import Flask

from api.reservation.views import init_reservation_routes
from api.swagger.views import init_swagger_routes
from api.tables.views import init_table_routes
from api.db import init_db, init_teardown

DATABASE = './api/db/TischResDB.db'


def init_routes(app):
    init_swagger_routes(app)
    init_reservation_routes(app)
    init_table_routes(app)


def create_app():  # pragma: no cover
    app = Flask(__name__)
    app.config['DATABASE'] = DATABASE
    init_routes(app)
    init_db(app)
    init_teardown(app)

    return app


if __name__ == "__main__":  # pragma: no cover
    flask_app = create_app()
    flask_app.run()
