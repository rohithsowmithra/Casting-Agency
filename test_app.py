import os
import unittest
import json
from app import app
from models import Movie, Actor

# get tokens from environment variables
assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN')
director_token = os.environ.get('CASTING_DIRECTOR_TOKEN')
producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')


# returns header based on user role specified
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
    """Setup test suite for the routes"""
    def setUp(self):
        """Setup application and database"""
        self.db_test_user = 'postgres'
        self.db_password = 'root'
        self.database_name = 'cast_agency'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.db_test_user,
            self.db_password,
            'localhost:5432',
            self.database_name
        )

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        """Executed after each test"""
        pass

    # test to fetch all movies
    def test_get_all_movies(self):
        response = self.client.get('/movies',
                                   headers=set_auth_header('assistant')
                                   )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['movies'])

    # test to check if unauthorized user can access movies endpoint
    def test_401_to_access_movies_unauthorized_user(self):
        response = self.client.get('/movies',
                                   headers=set_auth_header('')
                                   )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    # test to check if producer can create a movie
    def test_201_when_producer_adds_movie(self):
        data = {
            'title': 'Test-Movie-999',
            'release_date': '2000-01-01'
        }
        response = self.client.post('/movies',
                                    json=data,
                                    headers=set_auth_header('producer')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['movie'])

    # test to check that director can't create a movie
    def test_401_when_director_adds_movie(self):
        data = {
            'title': 'Test-Movie-100',
            'release_date': '01-01-2000'
        }
        response = self.client.post('/movies',
                                    json=data,
                                    headers=set_auth_header('director')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that assistant can't create a movie
    def test_401_when_assistant_adds_movie(self):
        data = {
            'title': 'Test-Movie-101',
            'release_date': '01-01-2000'
        }
        response = self.client.post('/movies',
                                    json=data,
                                    headers=set_auth_header('assistant')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that movie won't be created with bad args
    def test_400_when_adding_movie_with_invalid_args(self):
        data = {
            'title': 'Test-Movie99'
        }
        response = self.client.post('/movies',
                                    json=data,
                                    headers=set_auth_header('producer')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_data['success'], False)
        self.assertEqual(resp_data['message'], 'bad request')

    # test to check that producer can edit a movie
    def test_200_when_producer_edits_movie(self):
        data = {
            "title": "Test-Movie333",
            "release_date": "01-01-2001"
        }
        movie_id = Movie.query.first().id
        response = self.client.patch(f'/movies/{movie_id}',
                                     json=data,
                                     headers=set_auth_header('producer')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)

    # test to checkthat director can edit a movie
    def test_200_when_director_edits_movie(self):
        data = {
            "title": "Test-Movie444",
            "release_date": "01-01-2002"
        }
        movie_id = Movie.query.first().id
        response = self.client.patch(f'/movies/{movie_id}',
                                     json=data,
                                     headers=set_auth_header('director')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)

    # test to check that assistant can't edit a movie
    def test_401_when_assistant_edits_movie(self):
        data = {
            "title": "Test-Movie",
            "release_date": "01-01-2003"
        }
        movie_id = Movie.query.first().id
        response = self.client.patch(f'/movies/{movie_id}',
                                     json=data,
                                     headers=set_auth_header('assistant')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that movie can't be updated with invalid args
    def test_422_edit_movie_with_invalid_args(self):
        data = {
            "title": "",
            "release_date": ""
        }
        movie_id = Movie.query.first().id
        response = self.client.patch(f'/movies/{movie_id}',
                                     json=data,
                                     headers=set_auth_header('producer')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(resp_data['success'], False)

    # test to check that producer can delete a movie
    def test_200_when_producer_deletes_movie(self):
        data = {
            "title": "Test-Movie-999",
            "release_date": ""
        }
        self.client.post('/movies',
                         json=data,
                         headers=set_auth_header('producer')
                         )
        movie_id = Movie.query.first().id
        response = self.client.delete(f'/movies/{movie_id}', headers=set_auth_header('producer'))
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['movie'])

    # test to check that director can't delete a movie
    def test_401_when_director_deletes_movie(self):
        movie_id = Movie.query.first().id
        response = self.client.delete(f'/movies/{movie_id}',
                                      headers=set_auth_header('director')
                                      )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that assistant can't delete a movie
    def test_401_when_assistant_deletes_movie(self):
        movie_id = Movie.query.first().id
        response = self.client.delete(f'/movies/{movie_id}',
                                      headers=set_auth_header('assistant')
                                      )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that 404 is thrown if movie isn't found
    def test_404_when_deleting_unknown_movie(self):
        response = self.client.delete('/movies/91111',
                                      headers=set_auth_header('producer')
                                      )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(resp_data['success'], False)

    # test to fetch all actors
    def test_get_all_actors(self):
        response = self.client.get('/actors',
                                   headers=set_auth_header('assistant')
                                   )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['actors'])

    # test to check that unauthorized users can't access actors endpoint
    def test_401_to_access_actors_unauthorized_user(self):
        response = self.client.get('/actors',
                                   headers=set_auth_header('')
                                   )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    # test to check that producer can create an actor
    def test_201_producer_adding_actor(self):
        data = {
            'name': 'Test-Actor-499',
            'age': 35,
            'gender': 'Male'
        }
        response = self.client.post('/actors',
                                    json=data,
                                    headers=set_auth_header('producer')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['actor'])

    # test to check that director can add an actor
    def test_201_when_director_adds_actor(self):
        data = {
            'name': 'Test-Actor-500',
            'age': 30,
            'gender': 'Male'
        }
        response = self.client.post('/actors',
                                    json=data,
                                    headers=set_auth_header('director')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['actor'])

    # test to check that assistant can't create an actor
    def test_401_when_assistant_adds_actor(self):
        data = {
            'name': 'Actor101',
            'age': 25,
            'gender': 'Male'
        }
        response = self.client.post('/actors',
                                    json=data,
                                    headers=set_auth_header('assistant')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that actor cam't be created with bad args
    def test_400_when_adding_actor_with_invalid_args(self):
        data = {
            'name': 'Actor-102'
        }
        response = self.client.post('/actors',
                                    json=data,
                                    headers=set_auth_header('producer')
                                    )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_data['success'], False)
        self.assertEqual(resp_data['message'], 'bad request')

    # test to chedk that prodcuer can edit an actor
    def test_200_when_producer_edits_actor(self):
        data = {
            'name': 'Test-Actor-1',
            'age': 30,
            'gender': 'Male'
        }
        actor_id = Actor.query.first().id
        response = self.client.patch(f'/actors/{actor_id}',
                                     json=data,
                                     headers=set_auth_header('producer')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)

    # test to check that director can edit an actor
    def test_200_when_director_edits_actor(self):
        data = {
            'name': 'Test-Actor-2',
            'age': 40,
            'gender': 'FeMale'
        }
        actor_id = Actor.query.first().id
        response = self.client.patch(f'/actors/{actor_id}',
                                     json=data,
                                     headers=set_auth_header('director')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)

    # test to check that assistant can't edit actor's details
    def test_401_when_assistant_edits_actor(self):
        data = {
            'name': 'Test-Actor-3',
            'age': 45,
            'gender': 'FeMale'
        }
        actor_id = Actor.query.first().id
        response = self.client.patch(f'/actors/{actor_id}',
                                     json=data,
                                     headers=set_auth_header('assistant')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that actor's detailed can't be updated with invalid args
    def test_422_edit_movie_with_invalid_args(self):
        data = {
            'name': '',
            'age': '',
            'gender': ''
        }
        actor_id = Actor.query.first().id
        response = self.client.patch(f'/actors/{actor_id}',
                                     json=data,
                                     headers=set_auth_header('producer')
                                     )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(resp_data['success'], False)

    # test to check that producer can delete an actor
    def test_200_when_producer_deletes_actor(self):
        actor_id = Actor.query.first().id
        response = self.client.delete(f'/actors/{actor_id}',
                                      headers=set_auth_header('producer')
                                      )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)
        self.assertTrue(resp_data['actor'])

    # test to check that director can delete an actor
    def test_200_when_director_deletes_actor(self):
        actor_id = Actor.query.first().id
        response = self.client.delete(f'/actors/{actor_id}',
                                      headers=set_auth_header('director')
                                      )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['success'], True)

    # test to check that assistant can't delete an actor
    def test_401_when_assistant_deletes_actor(self):
        actor_id = Actor.query.first().id
        response = self.client.delete(f'/actors/{actor_id}',
                                      headers=set_auth_header('assistant')
                                      )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(resp_data['success'], False)

    # test to check that 404 is thrown when actor isn't found in database
    def test_404_when_deleting_unknown_actor(self):
        response = self.client.delete('/actors/91111',
                                      headers=set_auth_header('producer')
                                      )
        resp_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(resp_data['success'], False)


# Main method


if __name__ == "__main__":
    unittest.main()
