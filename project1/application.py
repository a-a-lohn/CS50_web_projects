import os

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
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
    if "user" in session:
      #uname = session["user"]
      return redirect(url_for("search"))

    return redirect(url_for("login"))

@app.route("/login", methods = ["GET", "POST"])
def login():
   if request.method == "POST":      
        # usernames are not case sensitive
        uname = request.form.get("username").lower() # or request.form["username"]
        pw = request.form.get("password")

        if not uname or not pw:
            flash("Please enter both a username and a password")
            return render_template("index.html")

        uname_present = User.query.filter(and_(User.username == uname, User.password == pw)).all()
        if not uname_present:
            flash("Incorrect username or password")
            return render_template("index.html")
      
        # if there are no issues with uname/pw, sign user in
        session["user"] = uname
        flash("Login successful")
        return redirect(url_for("index"))

   return render_template("login.html")

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
            # if there are no issues with uname/pw, sign user in
            flash("Registration successful")
            session["user"] = uname
            return redirect(url_for("index"))
        else:
            flash("Sorry! That username is already taken")
            #return render_template("register.html")  # this line is not needed

    return render_template("register.html")  

@app.route("/logout")
def logout():
   # remove the username from the session if it is there
   session.pop("user", None)
   flash("Logged out")
   return redirect(url_for("index"))

@app.route("/search")
def search():
    
    return render_template("search.html")