from sqlalchemy.sql import func
from config import app, db
from server.models.users import User

class Wish(db.Model):
    __tablename__ = 'wishes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship('User', foreign_keys=[user_id], backref="users_wishes")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())