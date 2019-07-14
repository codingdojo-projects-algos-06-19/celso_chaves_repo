from sqlalchemy.sql import func
from config import app, db
from server.models.users import User
from server.models.ideas_likes import likes_ideas_table

class Idea(db.Model):
    __tablename__ = 'ideas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(255))
    liked_by=db.relationship('User', secondary=likes_ideas_table, backref="liked_ideas")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())