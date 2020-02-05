from app import app
from models import db, User, Feedback


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

f1 = Feedback(
    title = "This is test feedback",
    content = "Test content",
    username = "user1"
)

f2 = Feedback(
    title = "This is test feedback, again",
    content = "Content test",
    username = "user2"
)

db.session.add_all([u1, u2, f1, f2])
db.session.commit()