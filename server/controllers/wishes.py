from flask import render_template, request, redirect, url_for, session, flash, Markup
from config import db, IntegrityError, desc, datetime
from server.models.users import User
from server.models.wishes import Wish
from server.models.grants import Grant
from datetime import date

def wishes(): 
    if 'user_id' in session:
        logged_in_user = User.query.get(session['user_id'])
        wish_list = Wish.query.filter_by(user_id=session['user_id']).all()
        granted_wishes = Grant.query.all()
        #granted_wishes_list = Wish.query.filter(Wish.wishes_grant.any(id=session['user_id'])).all()
        return render_template(
            'wishes.html',
            wish_list=wish_list, 
            user_list=User.query.all(), 
            logged_in_user=logged_in_user,
            granted_wishes=granted_wishes
        )
    else:
        flash('Please login to view your wishes!')
        return redirect('/portfolio/login')

def new_wish():
    if 'user_id' in session:
        logged_in_user = User.query.get(session['user_id'])
        return render_template(
            'new_wish.html',
            wish_list=logged_in_user, 
            user_list=User.query.all(), 
            logged_in_user=logged_in_user
        )
    else:
        flash('Please login or register to add wishes!')
        return redirect('/portfolio/login')

def create_wish():
    alerts = []
    if 'user_id' not in session:
        flash(Markup('Only registerd users can make a wish!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/wishes')
    
    if len(request.form['title']) < 1 and len(request.form['description']) < 1:
        alerts.append('Both fields most be provided!')
    else:
        if len(request.form['title']) < 1:
            alerts.append('A wish title most be provided')    
        if len(request.form['title']) < 3:
            alerts.append('A wish title must consist of at least 3 characters!')

        if len(request.form['description']) < 1:
            alerts.append('A description must be provided!')
        if len(request.form['description']) < 3:
            alerts.append('A description must consist of at least 3 characters!')

    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/wishes_app/new')
    
    new_wish = Wish(
        user_id = session['user_id'],
        title = request.form['title'],
        description = request.form['description']
    )
    print(request.form)
    db.session.add(new_wish)
    db.session.commit()
    flash('Your wish has been added to the list!')
    return redirect('/portfolio/wishes_app/wishes')

def edit_wish(id):
    if 'user_id' in session:
        get_wish = Wish.query.get(id)
        return render_template('edit_wish.html', 
        wish=get_wish, 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id'])
        )
    else:
        return redirect('/portfolio/wishes_app/wishes')

def update_wish(id):
    alerts = []
    if len(request.form['title']) < 3:
        alerts.append('A wish must consist of at least 3 characters!')

    if len(request.form['description']) < 3:
        alerts.append('A description must be provided!')
    
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/wishes_app/wishes')

    wish_update = Wish.query.get(id)
    wish_update.title = request.form['title']
    wish_update.description = request.form['description']
    db.session.commit()
    flash('Your wish has been updated!')
    return redirect('/portfolio/wishes_app/wishes')

def delete_wish(wish_id):
    wish_to_delete = Wish.query.get(id)
    db.session.delete(wish_to_delete)
    db.session.commit()
    flash('Your wish has been deleted!')
    return redirect('/portfolio/wishes_app/wishes')

def grant_wish(id):
    if 'user_id' not in session:
        flash(Markup('Only registerd users can grant a wish!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/wishes_app/wishes')
        
    new_grant = Grant(
        users_id = session['user_id'],
        wish_id = request.form['wish_id']
    )
    print(request.form)
    db.session.add(new_grant)
    db.session.commit()
    flash('Your wish has been granted!')
    return redirect('/portfolio/wishes_app/wishes')
