from config import app
from server.controllers import wishes

app.add_url_rule('/portfolio/wishes_app/wishes', view_func=wishes.wishes)
app.add_url_rule('/portfolio/wishes_app/new', view_func=wishes.new_wish)
app.add_url_rule('/portfolio/wishes_app/add_wish', view_func=wishes.create_wish, methods=['POST'])
#app.add_url_rule('/portfolio/wishes_app/wish/<id>', view_func=wishes.view_wish, methods=['GET'])
app.add_url_rule('/portfolio/wishes_app/wish/edit/<id>', view_func=wishes.edit_wish, methods=['GET'])
app.add_url_rule('/portfolio/wishes_app/wish/update/<id>', view_func=wishes.update_wish, methods=['POST'])
app.add_url_rule('/portfolio/wishes_app/wish/delete/<id>', view_func=wishes.delete_wish, methods=['POST'])
app.add_url_rule('/portfolio/wishes_app/wish/grant/<id>', view_func=wishes.grant_wish, methods=['POST'])