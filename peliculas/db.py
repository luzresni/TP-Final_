import psycopg2#lo que agregue
import psycopg2.extras#lo que agregue
import click
from flask import current_app, g


def get_db(): #aca es el import del get_db 
    if 'db' not in g:
        conn = psycopg2.connect(database="pelis",
                                host="127.0.0.1",
                                user="postgres",
                                password="postgres",
                                port="5432")

        
        #g.db.row_factory = dict_factory #aca hice la modificacion del get_db / remplazar por cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        g.db = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('films.sql') as f:
        db.execute(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


#agregue esto (7)
def dict_factory(cursor, row):
    """Arma un diccionario con los valores de la fila."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}