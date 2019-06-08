from config import app, render_template
from server.controllers import users 

app.add_url_rule('/portfolio/register', view_func=users.register)
app.add_url_rule('/portfolio/login_register', view_func=users.login_register)
app.add_url_rule('/portfolio/create_user', view_func=users.create_user, methods=['POST'])
app.add_url_rule('/portfolio/thankyou', view_func=users.thankyou)
app.add_url_rule('/portfolio/login', view_func=users.login)
app.add_url_rule('/portfolio/my_account', view_func=users.my_account)
app.add_url_rule('/portfolio/login_user', view_func=users.login_user, methods=['POST'])
app.add_url_rule('/portfolio/welcome', view_func=users.welcome_user)
app.add_url_rule('/portfolio/logout', view_func=users.logout_user)