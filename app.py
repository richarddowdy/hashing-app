from flask import Flask, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm, LoginForm
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
    
  

        new_user = User.register(username=username, 
                                password=password, 
                                email=email, 
                                first_name=first_name, 
                                last_name=last_name)
        
        db.session.add(new_user)
        db.session.commit()

        return redirect("/secret")

    else:
        return redirect("/register")


@app.route('/secret')
def secret():
    
    if "username" not in session:
        flash("Login first")
        return redirect("/login")
    else:
        return "YOU MADE IT!"
    
@app.route('/login', methods=['GET', 'POST'])
def login_form():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        current_user = User.authenticate(username , password)
        
        if current_user:
            session['username'] = current_user.username
            return redirect('/secret')

        else:
            form.username.errors = ["incorrect username/password"]
            return render_template("login.html", form=form)
        
    else:
        return render_template("login.html", form=form)


