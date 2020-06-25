import os

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
# Import table definitions
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = 'something simple for now'

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

# Tell Flask what SQLAlchemy database to use
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# DB CAN IDENTIFY NEW/EXISTING USERS, BUT APP MUST IDENTIFY WHO IS CURRENTLY LOGGED IN AND MUST INCLUDE A LOGOUT COMPONENT -- SESSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="POST":
        # usernames are not case sensitive
        uname = request.form.get("username").lower()
        pw = request.form.get("password")

        if not uname or not pw:
            flash("Please enter both a username and a password")
            return render_template("index.html")

        uname_present = User.query.filter(and_(User.username == uname, User.password == pw)).all()
        if not uname_present:
            flash("Incorrect username or password")
            return render_template("index.html")
        
        #return render_template("index.html", new_user=True) -- REMOVE THIS FROM index.html
        flash("Welcome back!")
        return redirect(url_for("search"), code=307) # POST request to /search

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        # usernames are not case sensitive
        uname = request.form.get("username").lower()
        pw = request.form.get("password")

        if not uname or not pw:
            flash("Please enter both a username and a password")
            return render_template("register.html")
        
        pw2 = request.form.get("password2")
        if pw != pw2:
            flash("Password attempts do not match")
            return render_template("register.html")
        
        uname_taken = User.query.filter(User.username == uname).all()
        if not uname_taken:
            user = User(username=uname, password=pw)
            db.session.add(user)
            db.session.commit()
            flash("Welcome!")
            return redirect(url_for("search"), code=307) # this code preserves the method type. See https://stackoverflow.com/questions/15473626/make-a-post-request-while-redirecting-in-flask
        else:
            flash("Sorry! That username is already taken")
            return render_template("register.html", exists=True) 

    return render_template("register.html")  

@app.route("/search", methods=["POST"])
def search():
    # the following should really be under /authentication
    # usernames are not case sensitive
    uname = request.form.get("username")
    if uname is None:
        return render_template("search.html")
    else:
        uname = uname.lower()
    '''pw = request.form.get("password")

    if not uname or not pw:
        # in cases like these, is it not better to somehow redirect to the page instead?
        # Not sure how to redirect AND set context variables
        return render_template("index.html", empty_field=True)

    uname_present = User.query.filter(and_(User.username == uname, User.password == pw)).all()
    if not uname_present:
        return render_template("index.html", invalid_user=True)
    '''
    #session[uname]
    return render_template("search.html")