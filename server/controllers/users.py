from flask import render_template, request, redirect, url_for, session, flash
from config import app
from server.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

def login_register():
    if 'user_id' not in session:
        return render_template('login_register.html')
    else:
        return redirect('/portfolio/register')

def register():
    if 'user_id' not in session:
        return render_template('register.html')
    else:
        return redirect('/portfolio/register')

def create_user():
    # @A1aaaaa
    alerts = User.validate(request.form)
    if len(alerts) > 0:
        print(len(alerts))
        if len(alerts) == 5:
            print(len(alerts))
            flash('All fields are required!')
            return redirect('/portfolio/login_register')    
        else:
            print(len(alerts))
            for alert in alerts:
                flash(alert)
            return redirect('/portfolio/login_register') 
    else:
        User.create(request.form)
        return redirect('/portfolio/thankyou')

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
    #return redirect('/portfolio/wishes_app/wishes')
    if 'user_id' not in session:
        return render_template('login.html', 
        user_list=User.query.all())
    else:
        return render_template('my_account.html', 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id']))

def login_user():
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
        return redirect('/portfolio/login_register')

    get_user_by_email = User.query.filter_by(email=request.form['email']).first()
    print('get_user_by_email', get_user_by_email)
    if get_user_by_email  != None:
        user = get_user_by_email
        if bcrypt.check_password_hash(user.password,request.form['password']):
            session['user_id'] = user.id
            return redirect('/portfolio/welcome')
    flash('The email or password is incorrect!')
    return redirect('/portfolio/login')

def welcome_user():
    if 'user_id' not in session:
       return redirect('/portfolio/login')
    print('session user id: ', session['user_id'])
    return render_template('welcome.html', 
    user_list=User.query.all(), 
    logged_in_user=User.query.get(session['user_id']))

def logout_user():
   session.pop('user_id', None)
   flash('Thanks for using our site!')
   return redirect(url_for('login'))



