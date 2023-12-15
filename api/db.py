import sqlite3
from flask import g

DATABASE = './TischResDB.db'
TESTING = False


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db




def init_db(app):
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    with app.app_context():
        db = get_db()
        with app.open_resource('create_buchungssystem.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False, commit = False):
    db = get_db()
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    if commit and not TESTING:  # pragma: no cover
        db.commit()

    return (rv[0] if rv else None) if one else rv
