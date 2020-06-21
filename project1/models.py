from flask_sqlalchemy import SQLAlchemy

# this creates the db reference object
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class Book(db.Model):
  __tablename__ = "book"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=True)