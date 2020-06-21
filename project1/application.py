import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
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

@app.route("/register", methods=["POST"])
def register():
    uname = request.form.get("username")
    pw = request.form.get("password1")
    user = User(username=uname, password=pw)
    db.session.add(user)
    db.session.commit()
    return render_template("register.html")

@app.route("/search", methods=["POST"])
def search():
    uname = request.form.get("username")
    pw = request.form.get("password")
    #verify that uname and pw are valid
    
    return render_template("search.html", name=uname)