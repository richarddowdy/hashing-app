from flask import Flask, render_template, redirect
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashing-app'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

bcrypt = Bcrypt()

app.config['SECRET_KEY'] = "SECRET KEY"

@app.route("/")
def root():
    return redirect("/register")


@app.route("/register")
def register_user_form():
    form = RegisterForm()
    return render_template("register.html", form=form)


@app.route("/register", methods = ["POST"])
def create_user():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
    
    hashed_password = bcrypt.generate_password_hash("password")

    new_user = User(username=username, 
                    password=hashed_password, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect("/secret")