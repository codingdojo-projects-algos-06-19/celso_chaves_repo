from flask import render_template, request, redirect, url_for, session, flash, Markup
from config import db, IntegrityError, desc
from server.models.ideas import Idea
from server.models.users import User
from server.models.ideas_likes import likes_ideas_table


def ideas():
    if 'user_id' in session:
        return render_template('ideas.html', 
        ideas_list=Idea.query.order_by(desc(Idea.id)), 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id'])
        )
    else:
        return render_template('login_register.html')

def create():
    alerts = []
    if 'user_id' not in session:
        flash(Markup('Only registerd users can create ideas!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/ideas_apps/bright_ideas')
    if len(request.form['content']) < 1:
        alerts.append('The idea cannot be blank!')

    if len(request.form['content']) < 3:
        alerts.append('The idea should be more than 3 characters')
           
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/ideas_app/bright_ideas')
    
    new_idea = Idea(
        content = request.form['content']
    )
    db.session.add(new_idea)
    db.session.commit()
    flash('Your brigh idea has been added!')
    return redirect('/portfolio/ideas_app/bright_ideas')

def view(id):
    idea_likes_list = Idea.query.filter(Idea.ideas_likes.any(id=id)).all()
    idea_list = Idea.query.all()
    if 'user_id' in session:
        return render_template(
            'idea_view.html',
            user_list=User.query.all(),
            idea_list=idea_list,
            logged_in_user=User.query.get(session['user_id']),
            idea_likes_list=idea_likes_list
            )
    else:
        return render_template(
            'idea_view.html', user_list=User.query.all())

def like_idea():
    existing_idea = Idea.query.get(request.form['ideas.id'])
    ideas_likes.append(existing_idea)
    if 'user_id' not in session:
        flash(Markup('Only registerd users can like ideas!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/ideas_app/bright_ideas/'+str(existing_idea.id)+'')
    try:
        db.session.commit()
        flash("The idea has been added!")
        return redirect('/portfolio/ideas_app/bright_ideas/'+str(existing_idea.id)+'')
    except IntegrityError:
        db.session.rollback()
        flash("You already liked this idea!")
        return redirect('/portfolio/ideas_app/bright_ideas/'+str(existing_idea.id)+'')

def edit(id):
    if 'user_id' in session:
        get_idea = Idea.query.get(id)
        return render_template('edit_idea.html', 
            idea=get_idea, 
            user_list=User.query.all(), 
            logged_in_user=User.query.get(session['user_id'])
        )
    else:
        return redirect('/portfolio/ideas_app/bright_ideas')

def update(id):
    alerts = []
    if len(request.form['content']) < 1:
        alerts.append('The idea cannot be blank!')

    if len(request.form['content']) < 3:
        alerts.append('The idea should be more than 3 characters!')
           
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        return redirect('/portfolio/ideas_app/bright_ideas')
    
    idea_update = Idea.query.get(id)
    idea_update.content = request.form['content']
    db.session.commit()
    flash('The idea has been updated!')
    return redirect('/portfolio/ideas_app/bright_ideas')

def delete(id):
    idea_to_delete = Idea.query.get(id)
    db.session.delete(idea_to_delete)
    db.session.commit()
    flash('The Idea has been deleted!')
    return redirect('/portfolio/ideas_app/bright_ideas')
