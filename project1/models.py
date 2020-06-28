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
  __searchable__ = ['isbn', 'title', 'author']  # these fields will be indexed by whoosh
  isbn = db.Column(db.String, primary_key=True)
  title = db.Column(db.String, nullable=False)
  author = db.Column(db.String, nullable=False)
  year = db.Column(db.Integer, nullable=False)

class Review(db.Model):
  __tablename__ = "review"
  # primary key is (isbn, reviewer) combination
  book_isbn = db.Column(db.String, db.ForeignKey("book.isbn"), primary_key=True)
  # cannot be anonymous, must leave a message, can leave a rating
  reviewer = db.Column(db.String, primary_key=True)
  message = db.Column(db.String, nullable=False)
  rating = db.Column(db.Integer, nullable=True)