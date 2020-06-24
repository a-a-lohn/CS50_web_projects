# run this code to create tables from models.py in the db

import os

from flask import Flask, render_template, request
# Import table definitions and db "object"
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()
    db.session.add(Book(isbn="123", title="test", author="me", year=2020))
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()