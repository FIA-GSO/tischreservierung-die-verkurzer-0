import sqlite3
import click
from flask import g, current_app, jsonify
from __main__ import app


DATABASE = '/TischResDB.db'

def init_db():
    db = get_db()
    with current_app.open_resource('create_buchungssystem.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@app.route("/dbtest", methods = ["GET"])
def dbtest():
    query = "SELECT * FROM reservierungen"
    conn = sqlite3.connect('TischResDB.db')
    cur = conn.cursor()

    results = cur.execute(query).fetchall()
    return jsonify(results)