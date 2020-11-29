import os
import unittest
import json
from app import app
from models import setup_db, Movie, Actor,db
from flask_sqlalchemy import SQLAlchemy

assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')

def set_auth_header(role):
    if role == 'assistant':
        return {'Authorization': 'Bearer {}'.format(assistant_token)}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(director_token)}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(producer_token)}
    elif role == '':
        return {'Authorization': ''}

class CastAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.db_test_user = 'postgres'
        self.db_password = 'root'
        self.database_name = 'cast_agency'
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.db_test_user, self.db_password, 'localhost:5432',
                                                             self.database_name)

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
        self.app = app
        self.client = app.test_client()
        #db.drop_all()
        #db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass


    def test_get_all_movies(self):
        response = self.client.get('/movies', headers=set_auth_header('assistant'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['movies'])

    def test_401_sent_unauthorized_user(self):
        response = self.client.get('/movies', headers=set_auth_header(''))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_add_movie(self):
        data = {
            'title': 'Test-Movie99',
            'release_date': '01-01-2000'
        }
        response = self.client.post('/movies', json=data, headers=set_auth_header('producer'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['movie'])


    def test_401_when_director_adds_movie(self):
        data = {
            'title': 'Test-Movie99',
            'release_date': '01-01-2000'
        }
        response = self.client.post('/movies', json=data, headers=set_auth_header('director'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)


    def test_401_when_assistant_adds_movie(self):
        data = {
            'title': 'Test-Movie99',
            'release_date': '01-01-2000'
        }
        response = self.client.post('/movies', json=data, headers=set_auth_header('assistant'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)


    def test_400_when_adding_movie_with_invalid_args(self):
        data = {
            'title': 'Test-Movie99'
        }
        response = self.client.post('/movies', json=data, headers={'Authorization': f'Bearer {producer_token}'})
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_data['success'], False)
        self.assertEqual(resp_data['message'], 'bad request')


    def test_200_when_producer_edit_movie(self):
        data = {
            "title": "Test-Movie",
            "release_date": "01-01-2001"
        }
        movie_id = Movie.query.filter(Movie.title == 'Test-Movie').first().id
        response = self.client.patch(f'/movies/{movie_id}', json=data, headers=set_auth_header('producer'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)


    def test_200_when_director_edit_movie(self):
        data = {
            "title": "Test-Movie1",
            "release_date": "01-01-2002"
        }
        movie_id = Movie.query.filter(Movie.title == 'Test-Movie1').first().id
        response = self.client.patch(f'/movies/{movie_id}', json=data, headers=set_auth_header('director'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)


    def test_401_when_assistant_edit_movie(self):
        data = {
            "title": "Test-Movie",
            "release_date": "01-01-2003"
        }
        movie_id = Movie.query.filter(Movie.title == 'Test-Movie').first().id
        response = self.client.patch(f'/movies/{movie_id}', json=data, headers=set_auth_header('assistant'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)


    def test_422_edit_movie_with_invalid_args(self):
        data = {
            "title": "",
            "release_date": ""
        }
        movie_id = Movie.query.filter(Movie.title == 'Test-Movie').first().id
        response = self.client.patch(f'/movies/{movie_id}', json=data, headers=set_auth_header('producer'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(resp_data['success'], False)


    def test_200_when_producer_deletes_movie(self):
        movie_id = Movie.query.filter(Movie.title == 'Test-Movie2').first().id
        response = self.client.delete(f'/movies/{movie_id}', headers=set_auth_header('producer'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['movie'])


    def test_401_when_director_deletes_movie(self):
        movie_id = Movie.query.first().id
        response = self.client.delete(f'/movies/{movie_id}', headers=set_auth_header('director'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    def test_401_when_assistant_deletes_movie(self):
        movie_id = Movie.query.first().id
        response = self.client.delete(f'/movies/{movie_id}', headers=set_auth_header('assistant'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)


    def test_404_when_deleting_unknown_movie(self):
        response = self.client.delete('/movies/91111', headers=set_auth_header('producer'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(resp_data['success'], False)


if __name__ == "__main__":
    unittest.main()