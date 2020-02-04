from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ connect to the database """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Users """

    __tablename__ = 'users'

    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False)

    password = db.Column(db.Text,
                         nullable=False)

    email = db.Column(db.String(50),
                      nullable=False)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)