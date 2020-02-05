from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

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
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        hashed= bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username,
                   password=hashed_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """ Validate user on login """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class Feedback(db.Model):   
    """Feedback from the user"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title= db.Column(db.String(100),
                     nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    username = db.Column(db.String,
                         db.ForeignKey('users.username'))
    user = db.relationship('User', backref='feedback')