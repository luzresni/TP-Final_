from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from peliculas.db import get_db

bp = Blueprint('language', __name__, url_prefix="/language/")


@bp.route('/')
def index():
    db = get_db()
    idiomas = db.execute(
          """SELECT name FROM language""" 

    ).fetchall()
    
    return render_template('lenguajes/index.html', idiomas=idiomas)
