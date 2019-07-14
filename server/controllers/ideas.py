from flask import render_template, request, redirect, url_for, session, flash, Markup
from config import db, IntegrityError, desc
from server.models.ideas import Idea
from server.models.users import User
from server.models.ideas_likes import likes_ideas_table
from server.models.users_ideas import users_ideas

def ideas_list():
    if 'user_id' in session:
        logged_in_user = User.query.get(session['user_id'])
        ideas_list = Idea.query.order_by(desc(Idea.id))
        ideas = Idea.query.join(User, Idea.user_id==User.id).add_columns(Idea.id, Idea.content, User.first_name, User.last_name, Idea.created_at, Idea.updated_at).order_by(desc(Idea.id))
        user_ideas_list = Idea.query.join(User, User.id==Idea.user_id)
        current_idea = Idea.query.get(1)
        # for a in user_ideas_list:
        #     print("USER_IDEAS_LIST: ", a.content)
        
        return render_template('partials/ideas_list.html',
        idea=current_idea,
        user_ideas_list=user_ideas_list, 
        ideas_list=ideas, 
        user_list=User.query.all(), 
        logged_in_user=User.query.get(session['user_id'])
        )
    else:
        flash('Register or login to view ideas!')
        return render_template('login_register.html')

def ideas():
    if 'user_id' in session:
        logged_in_user=User.query.get(session['user_id'])
        ideas = Idea.query.order_by(desc(Idea.id))
        user_ideas_list = Idea.query.join(User, User.id==Idea.user_id) 
        current_idea = Idea.query.get(1)
        # for idea in ideas:
        #     print(idea.user_id.liked_ideas)
        # liked_ideas = logged_in_user.liked_ideas
        # print(liked_ideas)
        # for a in user_ideas_list:
        #     print("USER_IDEAS_LIST: ", a.content)
        
        return render_template('ideas.html',
        idea=current_idea,
        user_ideas_list=user_ideas_list, 
        ideas_list=ideas, 
        user_list=User.query.all(), 
        logged_in_user=logged_in_user
        )
    else:
        flash('Register or login to view ideas!')
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
           
    print(request.form)
    if len(alerts) > 0:
        for alert in alerts:
            flash(alert)
        # return redirect('/portfolio/ideas_app/bright_ideas')
        return render_template('/partials/alerts.html'), 500

    new_idea = Idea(
        content = request.form['content'],
        user_id = request.form['user_id']
    )
    db.session.add(new_idea)
    db.session.commit()
    flash('Your brigh idea has been added!')
    return redirect('/portfolio/ideas_app/bright_ideas')

def view(id):
    existing_idea = Idea.query.get(id)
    existing_user = User.query.get(session['user_id'])
    # users_who_liked = likes_ideas_table.get(existing_idea).all()
    #idea_likes_list = Idea.query.filter(Idea.liked_by.any(id=id)).all() 
    # existing_user.liked_by
    # like_list = User.query.join(likes_ideas_table, likes_ideas_table.user_id==User.id) 
    # likes = likes_ideas_table
    # likes_2 = likes.user_id
    print('IDEA_LIKES_LIST: ', existing_user.liked_ideas)
    idea_list = Idea.query.all()
    current_idea = Idea.query.get(id)
    # print('IDEA: ', current_idea.id)
    if 'user_id' in session:
        return render_template(
            'idea_view.html',
            user_list=User.query.all(),
            idea=current_idea,
            idea_list=idea_list,
            logged_in_user=User.query.get(session['user_id'])
            )
    else:
        return render_template(
            'idea_view.html', user_list=User.query.all())

def like_idea(id):
    if 'user_id' not in session:
        flash(Markup('Only registerd users can like ideas!<br /><img src="/static/img/no-no.gif">'))
        return redirect('/portfolio/ideas_app/bright_ideas/'+str(existing_idea.id)+'')
    try:
        existing_idea = Idea.query.get(request.form['ideas_id'])
        existing_user = User.query.get(session['user_id'])
        existing_idea.liked_by.append(existing_user)
        db.session.commit()

        flash("Liked!")
        return redirect('/portfolio/ideas_app/bright_ideas')
    except IntegrityError:
        db.session.rollback()
        flash("You already liked this idea!")
        return redirect('/portfolio/ideas_app/bright_ideas')

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
