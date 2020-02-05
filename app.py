from flask import Flask, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, AddFeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashing-app'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

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

        return redirect(f"/user/{new_user.username}")

    else:
        # Can add feedback for errors
        return redirect("/register")


@app.route('/user/<username>')
def display_user(username):
    if "username" not in session or session["username"] != username:
        flash("Login first")
        return redirect("/login")
    else:
        user = User.query.filter_by(username=username).first()
        return render_template("user_page.html",user=user)
    
@app.route('/login', methods=['GET', 'POST'])
def login_form():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        current_user = User.authenticate(username , password)
        
        if current_user:
            session['username'] = current_user.username
            return redirect(f"/user/{current_user.username}")

        else:
            form.username.errors = ["incorrect username/password"]
            return render_template("login.html", form=form)
        
    else:
        return render_template("login.html", form=form)


@app.route("/logout")
def loggout_user():
    session.clear()
    return redirect("/")


@app.route("/user/<username>/feedback/add", methods = ["GET","POST"])
def add_feedback_form(username):
    form = AddFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title,content=content,username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/user/{username}")
    else:
        return render_template("feedback.html", form=form, username=username)
    

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def edit_feedback_form(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = AddFeedbackForm()

    if session['username'] == feedback.user.username:
        
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/user/{feedback.user.username}")
        else:
            return render_template("edit_feedback.html", form=form, feedback=feedback)
    else:
        login_form = LoginForm()
        return render_template("login.html", form=login_form)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if session['username'] == feedback.user.username:
        username = feedback.user.username
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/user/{username}")
    else:
        login_form = LoginForm()
        return render_template("login.html", form=login_form)