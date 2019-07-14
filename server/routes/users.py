from config import app, render_template
from server.controllers import users 

app.add_url_rule('/portfolio/user/register', view_func=users.register, endpoint='users:register')
app.add_url_rule('/portfolio/user/login_register', view_func=users.login_register, endpoint='users:login_register')
app.add_url_rule('/portfolio/user/create', view_func=users.create, endpoint='users:create', methods=['POST'])
app.add_url_rule('/portfolio/user/thankyou', view_func=users.thankyou, endpoint='users:thankyou')
app.add_url_rule('/portfolio/user/login', view_func=users.login, endpoint='users:login')
app.add_url_rule('/portfolio/user/my_account', view_func=users.my_account, endpoint='users:my_account')
app.add_url_rule('/portfolio/user/process_login', view_func=users.process_login, endpoint='users:process_login', methods=['POST'])
app.add_url_rule('/portfolio/user/welcome', view_func=users.welcome, endpoint='users:welcome')
app.add_url_rule('/portfolio/user/logout', view_func=users.logout, endpoint='users:logout')
app.add_url_rule('/portfolio/user/first_name', view_func=users.first_name, endpoint='users:first_name')
app.add_url_rule('/portfolio/user/update/<id>', view_func=users.update, endpoint='users:update', methods=['POST'])