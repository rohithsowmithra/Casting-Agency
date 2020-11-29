from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app
from models import db, Movie, Actor

migrate = Migrate(app, db)
manager = Manager(app)


# manager command to seed data. Command: "python manage.py seed"
@manager.command
def seed():
    """Creating initial few records in our database"""

    actor1 = Actor(name='Actor-1', age=35, gender='Male')
    actor2 = Actor(name='Actor-2', age=40, gender='Feale')
    actor3 = Actor(name='Actor-3', age=45, gender='Male')

    actor1.insert()
    actor2.insert()
    actor3.insert()

    movie1 = Movie(title='Movie-1', release_date='01-01-1970')
    movie2 = Movie(title='Movie-2', release_date='01-01-1975')
    movie3 = Movie(title='Movie-3', release_date='01-01-1980')

    movie1.actors = [actor1, actor2]
    movie2.actors = [actor2, actor3]
    movie3.actors = [actor3, actor1]

    movie1.insert()
    movie2.insert()
    movie3.insert()


manager.add_command('db', MigrateCommand)

# main method


if __name__ == '__main__':
    manager.run()
