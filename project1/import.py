# run this code to import books from books.csv into the db

import os

from flask import Flask
from models import db, Book
import csv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():

    f = open("books.csv")
    # books is a generator that, when next() is called, will split the row it yields after opening books.csv
    books = (row for row in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL))
    # skip over the row of column names
    next(books)
    for row in books:
        db.session.add(Book(isbn=row[0], title=row[1], author=row[2], year=row[3]))
    db.session.commit()

if __name__ == "__main__":
    # this is critical for the manipulation of the db within the app
    with app.app_context():
        main()