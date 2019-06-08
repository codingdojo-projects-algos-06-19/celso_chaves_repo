from flask import render_template, request, redirect, url_for, session, flash, Markup
from config import db, IntegrityError, desc
from server.models.users import User
from server.models.books import Book
from server.models.authors import Author

def books():
    if 'user_id' in session:
        return render_template(
            'books.html',
            book_list=Book.query.order_by(desc(Book.id)), 
            user_list=User.query.all(), 
            logged_in_user=User.query.get(session['user_id'])
        )
    else:
        return render_template(
            'books.html',
            book_list=Book.query.order_by(desc(Book.id))
        )

def create_book():
    alerts = []
    if 'user_id' not in session:
        flash(Markup('Only registerd users can add books!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/books_app/books')
    if len(request.form['title']) < 1:
        alerts.append('Please enter a title!')

    if len(request.form['description']) < 1:
        alerts.append('Please enter a book description!')
    
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/books_app/books')
    
    new_book = Book(
        title = request.form['title'],
        description = request.form['description']
    )
    print(new_book)
    db.session.add(new_book)
    db.session.commit()
    flash('The book has been added!')
    return redirect('/portfolio/books_app/books')

def view_book(id):
    authors_in_book = db.session.query(Book).filter_by(id=id).one()
    get_book = Book.query.get(id)
    author_list = Author.query.all()

    if 'user_id' in session:
        return render_template('book_view.html', book=get_book, authors=author_list, 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id']),
        authors_in_book=authors_in_book)
    else:
        return render_template(
            'book_view.html',
            book=get_book, 
            authors=author_list,
            authors_in_book=authors_in_book)

def add_book_to_author():
    existing_author = Author.query.get(request.form['author_id'])
    existing_book = Book.query.get(request.form['book_id'])
    print(existing_book.authors_and_books.append(existing_author))
    existing_book.authors_and_books.append(existing_author)
    if 'user_id' not in session:
        flash(Markup('Only registerd users can add books to authors!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/books_app/authors/'+str(existing_author.id)+'')
    try:
        db.session.commit()
        flash("The book has been added to the author's list")
        return redirect('/portfolio/books_app/authors/'+str(existing_author.id)+'')
    except IntegrityError:
        db.session.rollback()   
        flash("The book already exists in the author's book's list!")
        return redirect('/portfolio/books_app/authors/'+str(existing_author.id)+'')

def edit_book(id):
    if 'user_id' in session:
        get_book = Book.query.get(id)
        return render_template('edit_book.html', book=get_book, user_list=User.query.all(), logged_in_user=User.query.get(session['user_id'])
        )
    else:
        return redirect('/portfolio/books_app/books')

def update_book(id):
    alerts = []
    if len(request.form['title']) < 1:
        alerts.append('Please enter a title!')

    if len(request.form['description']) < 1:
        alerts.append('Please enter a book description!')
    
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/books_app/books')

    book_update = Book.query.get(id)
    book_update.title = request.form['title']
    book_update.description = request.form['description']
    db.session.commit()
    flash('The book has been updated!')
    return redirect('/portfolio/books_app/books')

def delete_book(id):
    book_count = Book.query.count()
    if book_count <= 1:
        flash(Markup('You cannot delete the last book in the database!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/books_app/books')
    book_instance_to_delete = Book.query.get(id)
    db.session.delete(book_instance_to_delete)
    db.session.commit()
    flash('The book has been deleted!')
    return redirect('/portfolio/books_app/books')
