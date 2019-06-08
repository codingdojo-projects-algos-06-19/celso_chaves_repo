from sqlalchemy.sql import func
from config import app, db
from server.models.books import Book
from server.models.books_authors import books_authors

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    notes = db.Column(db.String(255))
    authors_books_rel = db.relationship('Book', secondary=books_authors, backref=db.backref('authors_and_books', lazy='dynamic', cascade="all" ))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
