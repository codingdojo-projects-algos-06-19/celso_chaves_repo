from config import app, render_template
from server.controllers import root

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.add_url_rule('/portfolio', view_func=root.portfolio)
app.add_url_rule('/', view_func=root.index)