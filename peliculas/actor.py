from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
) #aca agruegue el jsonify
from werkzeug.exceptions import abort

from peliculas.db import get_db

bp = Blueprint('actor',__name__, url_prefix="/actor/")
bpapi = Blueprint('actor_api',__name__, url_prefix="/api/actor/")#aca duplique el prefijo


@bp.route('/')
def index():
    db = get_db()
    resultado = db.execute(
          """ SELECT first_name AS Nombre, last_name AS Apellido ,
           actor_id 
          FROM actor ORDER BY Nombre """ 

    )
    actors = resultado.fetchall()#aca ya esta modificado
    return render_template('actor/index.html', actors=actors)


#agregue una ruta con el api
@bpapi.route('/')
def index_api():
    db = get_db()
    actors = db.execute(
          """ SELECT first_name AS Nombre, last_name AS Apellido ,
           actor_id 
          FROM actor ORDER BY Nombre """ 

    ).fetchall() #modificar el fetchall()

    #agregue esto del for para el api
    for actor in actors:
        actor["url"] = url_for("actor_api.detalle_api", id=actor["actor_id"], _external=True)#se agrega el external para que se vea mas prolijo(?)

    return jsonify(actors=actors)#cambie el rendel_template por jsonify y borre las plantillas



@bp.route('/detalle/<int:id>')
def detalle(id):
    db = get_db()
    info_actor = db.execute( 
         """SELECT first_name, last_name FROM actor
         WHERE actor_id = ?;""", 
        (id,)).fetchone() #modificar el fetchall()
    
    peliculas = db.execute( 
        #aca hay que agregar 
         """ SELECT title, ac.film_id
         FROM film ac JOIN film_actor fia ON ac.film_id = fia.film_id  
         WHERE fia.actor_id = ?; """,
        (id,)).fetchall() #modificar el fetchall()
    



    return render_template('actor/detalle.html', info_actor=info_actor, peliculas=peliculas)

#esto tambien agregue. Es el Detalle con el api
@bpapi.route('/detalle/<int:id>')
def detalle_api(id):
    db = get_db()
    info_actor = db.execute( 
         """SELECT first_name, last_name FROM actor
         WHERE actor_id = ?;""", 
        (id,)).fetchone() #modificar el fetchall()
    
    peliculas = db.execute( 
        #aca hay que agregar 
         """ SELECT title, ac.film_id
         FROM film ac JOIN film_actor fia ON ac.film_id = fia.film_id  
         WHERE fia.actor_id = ?; """,
        (id,)).fetchall() #modificar el fetchall()
    
    for peli in peliculas:
        peli["url"] = url_for("pelis_api.detalle_api", id=peli["film_id"], _external=True)
    
    return jsonify(info_actor=info_actor, peliculas=peliculas)
