from flask import render_template, request, redirect, url_for, session, flash
from config import app, db
from server.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

def login_register():
    if 'user_id' not in session:
        return render_template('login_register.html')
    else:
        return redirect('/portfolio/user/register')

def register():
    if 'user_id' not in session:
        return render_template('register.html')
    else:
        return redirect('/portfolio/user/register')

def create():
    # @A1aaaaa
    alerts = User.validate(request.form)
    if len(alerts) > 0:
        print(len(alerts))
        if len(alerts) == 5:
            print(len(alerts))
            flash('All fields are required!')
            return redirect('/portfolio/user/register')    
        else:
            print(len(alerts))
            for alert in alerts:
                flash(alert)
            return redirect('/portfolio/user/register') 
    else:
        User.create(request.form)
        return redirect('/portfolio/user/thankyou')

def thankyou():
    if 'user_id' not in session:
        return render_template('register.html')
    else:
        return render_template('thankyou.html', 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id']))

def login():
    if 'user_id' in session:
        return render_template('welcome.html', 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id']))
    else:
        return render_template('login.html')

def my_account():
    #get_user_by_id = User.query.filter_by(id=session['user_id']).first()
    #return redirect('/portfolio/user/wishes_app/wishes')
    if 'user_id' not in session:
        return render_template('login.html', 
        user_list=User.query.all())
    else:
        return render_template('my_account.html', 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id']))

def process_login():
    alerts=[]
    # @A1aaaaa
    if len(request.form['email']) < 1:
        alerts.append('Please enter a email address')
    elif not EMAIL_REGEX.match(request.form['email']):
        alerts.append('Invalid email address!')
    if len(request.form['password']) < 1:
        alerts.append('Please enter a password')

    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/user/login_register')

    get_user_by_email = User.query.filter_by(email=request.form['email']).first()
    print('get_user_by_email', get_user_by_email)
    if get_user_by_email  != None:
        user = get_user_by_email
        if bcrypt.check_password_hash(user.password,request.form['password']):
            session['user_id'] = user.id
            return redirect('/portfolio/user/welcome')
    flash('The email or password is incorrect!')
    return redirect('/portfolio/user/login')

def update(id):
    alerts = []
    current_user = User.query.get(session['user_id'])
    print('CURRENT_USER: ', current_user.email)
    # Check if email is different from database
    if current_user.email == request.form['email']:
        if len(request.form['fname']) < 1:
            alerts.append('The first name field is required!')
        elif request.form['fname'].isalpha() != True:
            alerts.append('Only letters are allowed in the first name field!')

        if len(request.form['lname']) < 1:
            alerts.append('The last name field is required!')
        elif request.form['lname'].isalpha() != True:
            alerts.append('Only letters are allowed in the last name field!')

        if len(request.form['password']) > 0:
            if len(request.form['password']) < 8:
                alerts.append('The password needs to be at least 8 characters')
            elif not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", request.form['password']):
                alerts.append('The confirmed password must contain a number, a special character, upper and lowercase!')

            if len(request.form['password2']) < 1:
                alerts.append('The confirmed password cannot be blank!')

            if request.form['password'] != request.form['password2']:
                alerts.append('Both passwords should match')
    else:
        get_user_by_email = User.query.filter_by(email=request.form['email']).first()
        if get_user_by_email != None:
            alerts.append('This email address already exists! Please use a different one.')
        else:
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

    if len(alerts) > 0:
        if len(alerts) == 5:
            flash('All fields are required!')
            return redirect('/portfolio/user/my_account')
            # return render_template('/partials/alerts.html'), 500   
        else:
            for alert in alerts:
                flash(alert)
            # return redirect('/portfolio/user/my_account') 
            return render_template('partials/alerts.html'), 500
    else:
        user = User.query.get(id)
        user.first_name = request.form['fname']
        user.last_name = request.form['lname']
        user.email = request.form['email']

        db.session.commit()
        alerts.append('Your account has been updated!')
        for alert in alerts:
            flash(alert)
            print('ALERTS: ', alert)
        # return redirect('/portfolio/user/my_account')
        return render_template('partials/alerts-info.html', alerts=alerts)

def welcome():
    if 'user_id' not in session:
       return redirect('/portfolio/user/login')
    print('session user id: ', session['user_id'])
    return render_template('welcome.html', 
    user_list=User.query.all(), 
    logged_in_user=User.query.get(session['user_id']))

def logout():
   session.pop('user_id', None)
   flash('Thanks for using our site!')
   return redirect(url_for('users:login'))

def first_name():
    if 'user_id' not in session:
        return 'GUEST'
    else:
        user = User.query.get(session['user_id'])
        return user.first_name



