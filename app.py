"""Notes application."""

from flask import Flask, redirect, render_template, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from forms import AddUserForm, LoginUser
# import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def home():
    """Redirect to the register page"""
  
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = AddUserForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
    
        user = User.register(name, pwd, first_name, last_name, email)
        db.session.add(user)
        db.session.commit()

        session["username"] = name

        # on successful login, redirect to secret page
        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user."""

    form = LoginUser()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
    
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad name/password"]
        
    return render_template("login.html", form=form)


# @app.route("/secret", methods=["GET", "POST"])
# def secret():
#     """Redirect to the secret page"""
  
#     if 'user_name' in session:
#         render_template("secret.html")
#     else:
#         redirect("/login")


@app.route("/logout")
def logout():
    """Logout user."""

    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>")
def show_user(username):
    """Show user if logged in"""
    # breakpoint()
    if 'username' not in session or username != session["username"]:
        raise Unauthorized()
    else:
        user = User.query.get_or_404(username)
        return render_template("show_user.html", user=user)