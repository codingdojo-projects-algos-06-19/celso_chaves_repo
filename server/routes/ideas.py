from config import app
from server.controllers import ideas

app.add_url_rule('/portfolio/ideas_app/bright_ideas', view_func=ideas.ideas, endpoint="ideas:ideas")
app.add_url_rule('/portfolio/ideas_app/bright_ideas/list', view_func=ideas.ideas_list, endpoint="ideas:ideas_list")
app.add_url_rule('/portfolio/ideas_app/bright_ideas/<id>', view_func=ideas.view, methods=['GET'], endpoint="ideas:view")
app.add_url_rule('/portfolio/ideas_app/bright_ideas/create', view_func=ideas.create, methods=['POST'], endpoint="ideas:create")
app.add_url_rule('/portfolio/ideas_app/bright_ideas/edit/<id>', view_func=ideas.edit, methods=['GET'], endpoint="ideas:edit")
app.add_url_rule('/portfolio/ideas_app/bright_ideas/update/<id>', view_func=ideas.update, methods=['POST'], endpoint="ideas:update")
app.add_url_rule('/portfolio/ideas_app/bright_ideas/delete/<id>', view_func=ideas.delete, methods=['POST'], endpoint="ideas:delete")
app.add_url_rule('/portfolio/ideas_app/bright_ideas/like/<id>', view_func=ideas.like_idea, methods=['POST'], endpoint="ideas:like_idea")