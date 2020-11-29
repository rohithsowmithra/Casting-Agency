# Udac Casting Agency

## Introduction
This project is a capstone project for Udacity's Fullstack Nanodegree program. 
It models a company that is responsible for creating movies and managing and assigning actors to those movies. 
Only authorized users can interact with the APIs to view, add, update, delete the Movies and Actors.

This project is hosted on heroku and can be accessed from [here](https://udac-casting-agency.herokuapp.com/).

## Tech Stack
- Python3 and Flask as our server language and server framework
- HTML, CSS, Javascript and Bootstrap4 for our website's frontend
- SQLAlchemy ORM
- PostgreSQL as our database

## Getting Started

## Pre-requisites and Local Development
Developers using this project should already have python3 and pip installed. This uses [Auth0](https://auth0.com/) for authentication and authorization. So, developers working on this project should have an auth0 account.
Also, as this project is deployed on [Heroku](https://www.heroku.com/), it is advised tp create heroku account and setup the app for deployment.

## Dependencies
This project uses Flask to build the apis. Endpoints needs to be integrated with Auth0 for Authentication and Authorization. To start off with backend, install the requirements specified in requirements.txt.

### Installing Dependencies
#### Python
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
``` 
This will install all of the required packages we selected within the requirements.txt file.

#### Key Dependencies
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://flask.palletsprojects.com/en/1.1.x/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.
- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Authentication
APIs in this project can be accessed only by below users.
1. Assistant
```
email: assistant@udac.com
password: assistant@123
```
2. Director
```
email: director@udac.com
password: director@123
```
3. Producer
```
email: producer@udac.com
password: producer@123
```
Auh0 domain, audience etc can be found in setup.sh file in this directory.

## API Reference
### Error Handling
Errors are returned as JSON in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The APIs will return these error types when requests fail.
 - 400: bad request
 - 401: unauthorized
 - 404: resource not found
 - 422: unprocessable entity
 - 500: internal server error
 
### Endpoints
**GET /movies**
 - fetches all the movies from the database if the user has 'vie:movies' permission.
Sample Response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 01 Jan 1970 00:00:00 GMT",
            "title": "Movie-1"
        },
        {
            "id": 2,
            "release_date": "Wed, 01 Jan 1975 00:00:00 GMT",
            "title": "Movie-2"
        }
    ],
    "success": true
}
``` 
**POST /movies**
- creates a new movie if the user has 'add:movies' permission.
Sample Request:
```
{
  "title": "Movie-3",
  "release_date": "2020-01-01"
}
```
Sample Response:
```
{
  'success': true,
  'movie': 'Movie-3'
}
```
**PATCH /movies/<movie_id>**
- updates movie details if the user has 'update:movies' permission.
- request argument: movie_id: int
Sample Request:
```
{
  "title": "Movie-X",
  "release_date": "2022-01-01"
}
```
Sample Response:
```
{
  'success': true,
  'movie': {
              "id": 3,
              "title": "Movie-X",
              "release_date": "2022-01-01"
            }
}
```
**DELETE /movies/<movie_id>**
- deletes a movie from the database if the user has 'delete:movies' permission.
- request argument: movie_id: int
Sample Response:
```
{
  'success': true,
  'movie': 3
}
```
**GET /actors**
- fetches all actors from the database if the user has 'view:actors' permission.
Sample Response:
```
{
    "actors": [
        {
            "age": 35,
            "gender": "Male",
            "id": 1,
            "name": "Actor-1"
        },
        {
            "age": 40,
            "gender": "Female",
            "id": 2,
            "name": "Actor-2"
        }
    ],
    "success": true
}
```
**POST /actors**
- creates a new actor in database if user has 'add:actors' permission.
Sample Request:
```
{
    "name": "Actor-3",
    "age": 30,
    "gender": "Male"
}
```
Sample Response:
```
{
  'success': true,
  'actor': 'Actor-3'
}
```
**PATCH /actors/<actor_id>**
- updates actor's details in the database if the user has 'update:actors' permission.
- request argument: actor_id: int
Sample Request:
```
{
    "name": "Actor-X",
    "age": "45",
    "gender": "Male"
}
```
Sample Response:
```
{
  'success': true,
  "actors": [
        {
            "age": 45,
            "gender": "Male",
            "id": 1,
            "name": "Actor-X"
        }
}
```
**DELETE /actors/<actor_id>**
- deletes an actor from the database if the user has 'delete:actors' permission.
- request argument: actor_id:int
Sample Response:
```
{
  'success': true,
  'actor': 1
}
```

## Testing
To run the test, execute below commands:
```
python3 manage.py db upgrade
python3 manage.py seed
python3 test_app.py
```
Alternatively, you may also use the udac-casting-agency-pm-collection.json (postman collection) in this directory to run the unit tests.

## Authors
Rohith has authored all the files and and documentation (Readme.md) in this project.