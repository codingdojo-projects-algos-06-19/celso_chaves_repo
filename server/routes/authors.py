from config import app
from server.controllers import authors

app.add_url_rule('/portfolio/books_app/add_author_to_book', view_func=authors.add_author_to_book, endpoint='authors:add_author_to_book', methods=['POST'])
app.add_url_rule('/portfolio/books_app/authors', view_func=authors.authors, endpoint='authors:authors')
app.add_url_rule('/portfolio/books_app/authors/add', view_func=authors.create, endpoint='authors:create', methods=['POST'])
app.add_url_rule('/portfolio/books_app/authors/<id>', view_func=authors.view, endpoint='authors:view', methods=['GET'])
app.add_url_rule('/portfolio/books_app/authors/edit/<id>', view_func=authors.edit, endpoint='authors:edit', methods=['GET'])
app.add_url_rule('/portfolio/books_app/authors/update/<id>', view_func=authors.update, endpoint='authors:update', methods=['POST'])
app.add_url_rule('/portfolio/books_app/authors/delete/<id>', view_func=authors.delete, endpoint='authors:delete', methods=['POST'])