from flask import render_template, request, redirect, url_for, session, flash
from server.models.users import User
from server.models.books import Book

def page_not_found(error):
    return render_template('page_not_found.html'), 404

def portfolio():
    return render_template('portfolio.html')

def index():
    return render_template(
        'index.html',
        book_list=Book.query.all(), user_list=User.query.all()
    )
