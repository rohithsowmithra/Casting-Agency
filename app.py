import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import requires_auth
import json


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

    print(movie_id)

    movie = Movie.query.filter(Movie.id == movie_id).first()

    print(movie)

    try:
        if not movie:
            abort(404)

        if title:
            movie.title = title

        if release_date:
            movie.release_date = release_date

        movie.update()

    except Exception:
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

    try:
        movie = Movie.query.filter(Movie.id == movie_id).first()

        if not movie:
            abort(404)

        movie.delete()
    except Exception:
        abort(422)
    else:
        return jsonify({
            'success': True,
            'movie': movie_id
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)