import os
import unittest
import json
from app import create_app
from models import setup_db, Movie, Actor

assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')

class CastAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass


    def test_get_all_movies(self):
        response = self.client.get('/movies', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_401_sent_unauthorized_user(self):
        response = self.client.get('/movies', headers={'Authorization': ''})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)


    def test_add_movie(self):
        data = {
            'title': 'Test-Movie',
            'release_date': '01-01-2000'
        }
        response = self.client.post('/movies', json=data, headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])


    def test_401_unauthorized_add_movie(self):
        data = {
            'title': 'Test-Movie',
            'release_date': '01-01-2000'
        }
        response = self.client.post('/movies', json=data, headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)


    def test_400_sent_adding_movie(self):
        data = {
            'title': 'Test-Movie'
        }
        response = self.client.post('/movies', json=data, headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


