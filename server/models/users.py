from sqlalchemy.sql import func
from config import app, db, request, re, session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())        # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate(cls, form_info):
        print(form_info)
        alerts = []
        get_user_by_email = User.query.filter_by(email=request.form['email']).first()
        if get_user_by_email != None:
            alerts.append('This email address already exists! Please use a different one.')  

        if len(request.form['fname']) < 1:
            alerts.append('The first name field is required!')
        elif request.form['fname'].isalpha() != True:
            alerts.append('Only letters are allowed in the first name field!')

        if len(request.form['lname']) < 1:
            alerts.append('The last name field is required!')
        elif request.form['lname'].isalpha() != True:
            alerts.append('Only letters are allowed in the last name field!')
            
        if len(request.form['email']) < 1:
            alerts.append('The email address field is required!')
        elif not EMAIL_REGEX.match(request.form['email']):
            alerts.append('Invalid email address!')
                  
        if len(request.form['password']) < 1:
            alerts.append('The password cannot be blank!')
        elif len(request.form['password']) < 8:
            alerts.append('The password needs to be at least 8 characters')
        elif not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", request.form['password']):
            alerts.append('The confirmed password must contain a number, a special character, upper and lowercase!')
        
        if len(request.form['password2']) < 1:
            alerts.append('The confirmed password cannot be blank!')

        if request.form['password'] != request.form['password2']:
            alerts.append('Both passwords should match')
        return alerts

    @classmethod
    def create(cls, form):
        #@A1aaaaa
        pw_hash = bcrypt.generate_password_hash(request.form['password']) 
        new_user = User(
            first_name = request.form['fname'],
            last_name = request.form['lname'],
            email = request.form['email'],
            password = pw_hash
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        print('SESSION_ID: ', session['user_id'])
        return new_user.id