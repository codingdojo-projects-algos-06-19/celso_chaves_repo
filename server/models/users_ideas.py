from config import db


# This table is tested and working.
# Many to Many / User and KART and Item
users_ideas = db.Table('users_ideas',
                        db.Column('user_id', db.Integer,
                                  db.ForeignKey('users.id'),
                                  primary_key=True),
                        db.Column('idea_id', db.Integer,
                                  db.ForeignKey('ideas.id'),
                                  primary_key=True))