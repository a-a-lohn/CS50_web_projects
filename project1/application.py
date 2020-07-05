# FIND OUT WHERE PYTHON MODULES ARE GETTING INSTALLED

import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine, and_, or_
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
app.secret_key = 'something simple for now' # needed for session?

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

# Tell Flask what SQLAlchemy database to use
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# prevent app from sorting jsonified data
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def index():
    if "user" in session:
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
            return render_template("login.html")

        # the table name may be 'user', but the object name in models.py is 'User'
        uname_present = User.query.filter(and_(User.username == uname, User.password == pw)).all()
        if not uname_present:
            flash("Incorrect username or password")
            return render_template("login.html")
      
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
        # if there are no issues with uname/pw, add user and sign user in
        if not uname_taken:
            user = User(username=uname, password=pw)
            db.session.add(user)
            db.session.commit()
            flash("Welcome!")
            session["user"] = uname
            return redirect(url_for("index"))
        else:
            flash("Sorry! That username is already taken")
            return render_template("register.html")  # this line is not needed, but makes more sense to put

    return render_template("register.html")  

@app.route("/logout", methods=["POST", "GET"]) # get should just redirect to prevent error
def logout():
    if request.method != "POST":
        return redirect(url_for("index"))
    # remove the username from the session if it is there
    session.pop("user", None)
    flash("Logged out")
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" in session:
        if request.method == "POST":
            # get the search value inputted by user and display results
            # ilike function is case-insensitive
            search = request.form.get("book_search")
            if search:
                books = Book.query.filter(or_(Book.author.ilike("%"+search+"%"), \
                    Book.title.ilike("%"+search+"%"), \
                    Book.isbn.ilike("%"+search+"%"))).all()
            else: books=[]
            flash(str(len(books)) + " results")
            if not books:
                flash("No books found")
            return render_template("search.html", books=books)

        return render_template("search.html")

    flash("Please login first")
    return redirect(url_for("login"))

# this route extracts variable data from the URL using a GET request - the function arguments correspond to URL data
# isbn can technically have the char X, so it is a string, not an int
@app.route("/search/<string:book_isbn>")
def book(book_isbn):
    if "user" in session:
        book = Book.query.get(book_isbn)
        reviews = Review.query.filter_by(book_isbn=book_isbn)
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ys0hBNpiMjxTgKdVpJBVUw", "isbns": book_isbn})
        if res.status_code != 200:
            rating = "Not available"
        else:
            data = res.json()
            rating = data['books'][0]['average_rating']
        # if user already reviewed this book, do not let them review it again
        if session["user"] in [review.reviewer for review in reviews]:
            return render_template("book.html", book=book, rating=rating, reviews=reviews, already_reviewed=True)
        return render_template("book.html", book=book, rating=rating, reviews=reviews)
    
    flash("Please login first")
    return redirect(url_for("login"))

@app.route("/search/<string:book_isbn>/review", methods=["GET", "POST"])
def review(book_isbn):
    if "user" in session:
        book = Book.query.get(book_isbn)
        if request.method == "POST":
            message = request.form.get("message")
            rating = request.form.get("rating")
            review = Review(book_isbn=book_isbn, reviewer=session["user"], message=message, rating=rating)
            db.session.add(review)
            db.session.commit()
            flash("Review added")
        return render_template("review.html", book=book)

@app.route("/api/<string:book_isbn>")
def book_api(book_isbn):
    book = Book.query.get(book_isbn)
    if book is None:
        # make a page instead
        return jsonify({"error": "Invalid isbn"}), 404
    
    reviews = Review.query.filter_by(book_isbn=book_isbn)
    num_reviews = Review.query.filter_by(book_isbn=book_isbn).count()
    avg_score = sum([review.rating for review in reviews])/num_reviews
    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": num_reviews,
            "average_score": avg_score
            })

if __name__ == '__main__':
    app.run()