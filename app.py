import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import requires_auth, AuthError
import json
import sys


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  app.config['SECRET_KEY'] = 'dev'

  CORS(app, resources={r"/.*": {"origins": "*"}})

  return app

app = create_app()


@app.after_request
def after_request(response):

  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')

  return response


@app.route('/')
def index():
  auth_server_details = {
    'auth_host': os.environ.get('AUTH0_DOMAIN'),
    'audience': os.environ.get('API_AUDIENCE'),
    'client_id': os.environ.get('CLIENT_ID'),
    'redirect_url': os.environ.get('AUTH0_REDIRECT_URL')
  }
  print("auth server details are: "+json.dumps(auth_server_details))
  return render_template('index.html', auth_server_details = auth_server_details)


@app.route('/movies', methods = ['GET'])
@requires_auth('view:movies')
def get_all_movies(payload):
  try:
    all_movies = Movie.query.all()
    movies = [movie.format() for movie in all_movies]
    return jsonify({
      'success': True,
      'movies': movies
      }), 200
  except Exception:
      print(sys.exc_info())
      abort(422)


@app.route('/movies', methods = ['POST'])
@requires_auth('add:movies')
def add_movie(payload):
    body = request.get_json()

    if not body:
        abort(400)

    if not ('title' in body and 'release_date' in body):
        abort(400)

    title = body['title']
    release_date = body['release_date']

    try:
        movie = Movie(title=title, release_date = release_date)
        movie.insert()
    except Exception:
        print(sys.exc_info())
        abort(422)
    else:
        return jsonify({
            'success': True,
            'movie': title
            }), 201


@app.route('/movies/<int:movie_id>', methods = ['PATCH'])
@requires_auth('update:movies')
def update_movie(payload, movie_id):
    body = request.get_json()

    if not body:
        abort(400)

    if not ('title' in body or 'release_date' in body):
        abort(400)

    title = body['title']
    release_date = body['release_date']
    movie = Movie.query.filter(Movie.id == movie_id).first()

    if not movie:
        abort(404)

    if title == '' and release_date == '':
        abort(422)

    try:
        if title:
            movie.title = title

        if release_date:
            movie.release_date = release_date

        movie.update()

    except Exception:
        print(sys.exc_info())
        movie.rollback()
        abort(422)
    else:
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200


@app.route('/movies/<int:movie_id>', methods = ['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):

    movie = Movie.query.filter(Movie.id == movie_id).first()

    if not movie:
        abort(404)

    try:
        movie.delete()
    except Exception:
        print(sys.exc_info())
        abort(422)
    else:
        return jsonify({
            'success': True,
            'movie': movie_id
        }), 200


@app.route('/actors', methods = ['GET'])
@requires_auth('view:actors')
def get_all_actors(payload):
    try:
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200
    except Exception:
        print(sys.exc_info())
        abort(422)


@app.route('/actors', methods = ['POST'])
@requires_auth('add:actors')
def add_actor(payload):
    body = request.get_json()

    if not body:
        abort(400)

    if not ('name' in body and 'age' in body and 'gender' in body):
        abort(400)

    name = body['name']
    age = body['age']
    gender = body['gender']

    try:
        actor = Actor(name = name, age = age, gender = gender)
        actor.insert()
    except Exception:
        print(sys.exc_info())
        abort(422)
    else:
        return jsonify({
            'success': True,
            'actor': name
        }), 201


@app.route('/actors/<int:actor_id>', methods = ['PATCH'])
@requires_auth('update:actors')
def update_actor(payload, actor_id):
    body = request.get_json()

    if not body:
        abort(400)

    if not ('name' in body or 'age' in body or 'gender' in body):
        abort(400)

    name = body['name']
    age = body['age']
    gender = body['gender']

    actor = Actor.query.filter(Actor.id == actor_id).first()

    if not actor:
        abort(404)

    if name == '' and age == '' and gender == '':
        abort(422)

    try:
        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender

        actor.update()

    except Exception:
        print(sys.exc_info())
        actor.rollback()
        abort(422)
    else:
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200


@app.route('/actors/<int:actor_id>', methods = ['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).first()

    if not actor:
        abort(404)

    try:
        actor.delete()
    except Exception:
        print(sys.exc_info())
        abort(422)
    else:
        return jsonify({
            'success': True,
            'actor': actor_id
        }), 200


# Error Handlers


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable entity'
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'successs': False,
        'code': 500,
        'message': 'internal server error'
    }), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'code': error.status_code,
        'message': error.error
    }), error.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)