from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from peliculas.db import get_db

bp = Blueprint('category', __name__, url_prefix="/category/")


@bp.route('/')
def index():
    db = get_db()
    categoria = db.execute(
          """SELECT c.name FROM category c ORDER BY c.name""" 

    ).fetchall()

    return render_template('categoria/index.html', categoria=categoria)
