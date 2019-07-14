from config import app
from server.controllers import wishes

app.add_url_rule('/portfolio/wishes_app/wishes', view_func=wishes.wishes, endpoint='wishes:wishes')
app.add_url_rule('/portfolio/wishes_app/new', view_func=wishes.new, endpoint='wishes:new')
app.add_url_rule('/portfolio/wishes_app/add_wish', view_func=wishes.create, endpoint='wishes:create', methods=['POST'])
#app.add_url_rule('/portfolio/wishes_app/wish/<id>', view_func=wishes.view_wish, methods=['GET'])
app.add_url_rule('/portfolio/wishes_app/wish/edit/<id>', view_func=wishes.edit, endpoint='wishes:edit', methods=['GET'])
app.add_url_rule('/portfolio/wishes_app/wish/update/<id>', view_func=wishes.update, endpoint='wishes:update', methods=['POST'])
app.add_url_rule('/portfolio/wishes_app/wish/delete/<id>', view_func=wishes.delete, endpoint='wishes:delete', methods=['POST'])
app.add_url_rule('/portfolio/wishes_app/wish/grant/<id>', view_func=wishes.grant, endpoint='wishes:grant', methods=['POST'])