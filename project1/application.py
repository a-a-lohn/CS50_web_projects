import os

from flask import Flask, session, render_template, request, redirect, url_for
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

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

# Tell Flask what SQLAlchemy database to use
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/authentication", methods=["POST"])
def authentication():
    uname = request.form.get("username")
    pw = request.form.get("password")

    if not uname or not pw:
        return render_template("register.html", empty_field=True)
    
    pw2 = request.form.get("password2")
    if pw != pw2:
        return render_template("register.html", mismatch=True)
    
    uname_taken = User.query.filter(User.username == uname).all()
    if not uname_taken:
        user = User(username=uname, password=pw)
        db.session.add(user)
        db.session.commit()
        # can't redirect to search b/c it only accepts posts requests. figure out a way around this
        # see https://stackoverflow.com/questions/17057191/redirect-while-passing-arguments
        return redirect(url_for("index", empty_field=True))
    else:
        return render_template("register.html", exists=True)   

@app.route("/search", methods=["POST"])
def search():
    uname = request.form.get("username")
    pw = request.form.get("password")

    if not uname or not pw:
        return render_template("index.html", empty_field=True)

    uname_present = User.query.filter(and_(User.username == uname, User.password == pw)).all()
    if not uname_present:
        return render_template("index.html", invalid_user=True)

    return render_template("search.html", name=uname)