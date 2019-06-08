from flask import render_template, request, redirect, url_for, session, flash, Markup
from config import db, IntegrityError, desc
from server.models.users import User
from server.models.books import Book
from server.models.authors import Author
from server.models.wishes import Wish

def authors():
    if 'user_id' in session:
        return render_template('authors.html', 
        author_list=Author.query.order_by(desc(Author.id)), 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id'])
        )
    else:
        return render_template('authors.html', author_list=Author.query.order_by(desc(Author.id)))

def create():
    alerts = []
    if 'user_id' not in session:
        flash(Markup('Only registerd users can add authors!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/books_app/books')
    if len(request.form['fname']) < 1:
        alerts.append('Please enter a first name!')
    elif request.form['fname'].isalpha() != True:
        alerts.append('Only letters are allowed in the first name field!')

    if len(request.form['lname']) < 1:
        alerts.append('Please enter a last name!')
    elif request.form['lname'].isalpha() != True:
        alerts.append('Only letters are allowed in the last name field!')
           
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/books_app/authors')
    
    new_author = Author(
        first_name = request.form['fname'],
        last_name = request.form['lname'],
        notes = request.form['notes']
    )
    print(new_author)
    db.session.add(new_author)
    db.session.commit()
    flash('The Author has been added!')
    return redirect('/portfolio/books_app/authors')

def view(id):
    author_book_list = Book.query.filter(Book.authors_and_books.any(id=id)).all()
    get_author = Author.query.get(id)
    book_list = Book.query.all()
    if 'user_id' in session:
        return render_template(
            'author_view.html',
            author=get_author, 
            user_list=User.query.all(),
            book_list=book_list,
            logged_in_user=User.query.get(session['user_id']),
            author_book_list=author_book_list)
    else:
        return render_template(
            'author_view.html',
                        author=get_author, 
                        user_list=User.query.all(),
                        book_list=Book.query.all(),
                        author_book_list=author_book_list)

def add_author_to_book():
    existing_author = Author.query.get(request.form['author_id'])
    existing_book = Book.query.get(request.form['book_id'])
    existing_book.authors_and_books.append(existing_author)
    if 'user_id' not in session:
        flash(Markup('Only registerd users can add authors to books!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/books_app/books/'+str(existing_book.id)+'')
    try:
        db.session.commit()
        flash("The author has been added to the book's list")
        return redirect('/portfolio/books_app/books/'+str(existing_book.id)+'')
    except IntegrityError:
        db.session.rollback()
        flash("The author already exists in the book's author's list!")
        return redirect('/portfolio/books_app/books'+str(existing_book.id)+'')

def edit(id):
    if 'user_id' in session:
        get_author = Author.query.get(id)
        return render_template('edit_author.html', author=get_author, user_list=User.query.all(), logged_in_user=User.query.get(session['user_id'])
        )
    else:
        return redirect('/portfolio/books_app/authors')

def update(id):
    alerts = []
    if len(request.form['fname']) < 1:
        alerts.append('Please enter a first name!')
    elif request.form['fname'].isalpha() != True:
        alerts.append('Only letters are allowed in the first name field!')

    if len(request.form['lname']) < 1:
        alerts.append('Please enter a last name!')
    elif request.form['lname'].isalpha() != True:
        alerts.append('Only letters are allowed in the last name field!')
           
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/books_app/authors')
    
    author_update = Author.query.get(id)
    author_update.first_name = request.form['fname']
    author_update.last_name = request.form['lname']
    author_update.notes = request.form['notes']
    db.session.commit()
    flash('The Author has been updated!')
    return redirect('/portfolio/books_app/authors')

def delete(id):
    author_count = Author.query.count()
    if author_count <= 1:
        flash(Markup('You cannot delete the last author in the database!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/books_app/authors')
    author_instance_to_delete = Author.query.get(id)
    db.session.delete(author_instance_to_delete)
    db.session.commit()
    flash('The Author has been deleted!')
    return redirect('/portfolio/books_app/authors')
