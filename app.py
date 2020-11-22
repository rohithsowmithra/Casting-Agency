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


@app.route('/movies')
@requires_auth('view:movies')
def get_all_movies():
  try:
    all_movies = Movie.query.all()
    movies = [movie.format() for movie in all_movies]
    return jsonify({
      'success': True,
      'movies': movies
      })
  except Exception:
    abort(422)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)