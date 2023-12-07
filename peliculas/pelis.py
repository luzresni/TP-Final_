from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from peliculas.db import get_db

bp = Blueprint('pelis', __name__, url_prefix="/pelis/")
bpapi = Blueprint('pelis_api',__name__, url_prefix="/api/pelis/")#modificar


@bp.route('/')
def index():
    db = get_db()
    db.execute( 
         """SELECT f.film_id, f.title, f.release_year, l.name AS idioma FROM film f JOIN language l
            ON f.language_id = l.language_id
            ORDER BY title """ 
 #       SELECT Title AS TITULO FROM albums
 #   WHERE ArtistId = (SELECT ArtistId FROM artists
 #                   WHERE name = "Deep Purple")

   #"""SELECT f.title, f.release_year, "ingles" AS idioma 
        #FROM film f ORDER BY title """

    )
    peliculas = db.fetchall()#hasta aca en pelis.py
    return render_template('pelis/index.html', peliculas=peliculas) #CREO QUE ACA SE AGREGAN LAS TABLAS

@bpapi.route('/') #modificar
def index_api():
    db = get_db()
    db.execute( #agregar esto
         """SELECT f.film_id, f.title, f.release_year, l.name AS idioma FROM film f JOIN language l
            ON f.language_id = l.language_id
            ORDER BY title """ 
    )
    peliculas = db.fetchall()   
    for peli in peliculas:
        peli["url"] = url_for("pelis_api.detalle_api", id=peli["film_id"], _external=True)#se agrega el external para que se vea mas prolijo(?)
    

    return jsonify(peliculas=peliculas)




#HACER ESTO MISMO PERO EN ACTOR.PY(CREO9) ADEMAS AGREGAR EL URL, COMO EN EL ACTOR
@bp.route('/detalle/<int:id>')
def detalle(id):
    db = get_db()
    info_peli = db.execute( 
         """SELECT fi.title, fi.description, fi.release_year FROM film fi
         WHERE fi.film_id = ?""", 
        (id,)).fetchone() #modificar el fetchone 
    
    actors = db.execute( 
         """ SELECT ac.first_name, ac.last_name, ac.actor_id
         FROM actor ac JOIN film_actor fia ON ac.actor_id = fia.actor_id  
         WHERE fia.film_id = ?;""",
        (id,)).fetchall() #modificar el fetchone
    



    return render_template('pelis/detalle.html', info_peli=info_peli, actors=actors)



@bpapi.route('/detalle/<int:id>')
def detalle_api(id):
    db = get_db()
    info_peli = db.execute( 
         """SELECT fi.title, fi.description, fi.release_year FROM film fi
         WHERE fi.film_id = ?""", 
        (id,)).fetchone() #creo que tambien el aca modificar el fetchone
    
    actors = db.execute( 
         """ SELECT ac.first_name, ac.last_name, ac.actor_id
         FROM actor ac JOIN film_actor fia ON ac.actor_id = fia.actor_id  
         WHERE fia.film_id = ?;""",
        (id,)).fetchall()#creo que tambien el aca modificar el fetchone
    

    for actor in actors:
        actor["url"] = url_for("actor_api.detalle_api", id=actor["actor_id"], _external=True)#se agrega el external para que se vea mas prolijo(?)


    return jsonify(info_peli=info_peli, actors=actors)




















#ACA YA AGREGUE LENGUAJE, ME FALTA ACTOR Y CATEGORIA.


# def get_post(id):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     return post



