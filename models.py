import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, Table, ForeignKey

db = SQLAlchemy()
db_path = os.environ.get('DATABASE_URL')

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, db_path=db_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
movies_actors table
'''


movies_actors = Table('movies_actors', db.Model.metadata,
                      Column('movie_id', Integer,
                             ForeignKey('movie.id'),
                             primary_key=True),
                      Column('actor_id', Integer,
                             ForeignKey('actor.id'),
                             primary_key=True)
                      )


'''
movie table
'''


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    release_date = Column(DateTime, nullable=False)
    actors = db.relationship('Actor',
                             secondary=movies_actors,
                             backref='movies',
                             lazy=True
                             )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]
        }

    def __repr__(self):
        return f"< Movie {self.id}, {self.title}>"


'''
actor table
'''


class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.title for movie in self.movies]
        }

    def __repr__(self):
        return f"<Actor {self.id}, {self.name}>"
