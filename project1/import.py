# run this code to create import book from books.csv into the db

import os

from flask import Flask
from models import db, Book

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    #LOOK AT BEER EXAMPLE TO SEE HOW THIS CAN BE DONE WITH GENERATORS
    books = open("books.csv")
    book.readline
    #for row in books:
    #    row = row.split(",")
    #    db.session.add(Book(isbn=row[0], title=row[1], author=row[2] year=row[3][:3]))
    #db.session.commit()

if __name__ == "__main__":
    # this is critical for the manipulation of the db within the app
    with app.app_context():
        main()