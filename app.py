from flask import Flask, render_template, redirect
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashing-app'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

app.config['SECRET)KEY'] = "SECRET KEY"

# @app.route("/")
# def root():
