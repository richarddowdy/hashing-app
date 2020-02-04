from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User(
    username="user1",
    password="large",
    email=5,
    first_name="kevin",
    last_name="steve"
)

u2 = User(
    username="user2",
    password="large",
    email=5,
    first_name="jason",
    last_name="michael"
)

db.session.add_all([u1, u2])
db.session.commit()