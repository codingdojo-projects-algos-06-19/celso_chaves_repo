from sqlalchemy.sql import func
from config import app, db

books_authors = db.Table('books_authors', 
              db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True), 
              db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True))