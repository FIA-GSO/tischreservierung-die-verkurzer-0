import os
import sqlite3
from flask import current_app
from flask import g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )

        def make_dicts(cursor, row):
            return dict((cursor.description[idx][0], value)
                        for idx, value in enumerate(row))

        g.db.row_factory = make_dicts

    return g.db


def init_db(app):
    with app.app_context():
        db = get_db()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(base_dir, 'create_buchungssystem.sql')
        with app.open_resource(sql_path, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def close_db(e=None):  # pragma: no cover
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_teardown(app):  # pragma: no cover
    """Register database functions with the Flask app. This is called by
       the application factory.
       """
    app.teardown_appcontext(close_db)


def query_db(query, args=(), one=False):
    db = get_db()
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    db.commit()

    return (rv[0] if rv else None) if one else rv
