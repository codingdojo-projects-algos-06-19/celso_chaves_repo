from config import app
from server.controllers import books 

app.add_url_rule('/portfolio/books_app/books', view_func=books.books)
app.add_url_rule('/portfolio/books_app/add_book', view_func=books.create_book, methods=['POST'])
app.add_url_rule('/portfolio/books_app/books/<id>', view_func=books.view_book, methods=['GET'])
app.add_url_rule('/portfolio/books_app/books/edit/<id>', view_func=books.edit_book, methods=['GET'])
app.add_url_rule('/portfolio/books_app/books/update/<id>', view_func=books.update_book, methods=['POST'])
app.add_url_rule('/portfolio/books_app/books/delete/<id>', view_func=books.delete_book, methods=['POST'])
app.add_url_rule('/portfolio/books_app/add_book_to_author', view_func=books.add_book_to_author, methods=['POST'])