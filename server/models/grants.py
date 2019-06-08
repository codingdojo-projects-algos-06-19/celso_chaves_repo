from sqlalchemy.sql import func
from config import app, db

class Grant(db.Model):
    __tablename__ = 'grants'
    id = db.Column(db.Integer, primary_key=True)
    wish_id = db.Column(db.Integer, db.ForeignKey("wishes.id"))
    wish_grant = db.relationship("Wish", foreign_keys=[wish_id], backref="wishes_grant", cascade="all")
    users_id = db.Column(db.Integer, db.ForeignKey("users.id")) 
    user_grant = db.relationship("User", foreign_keys=[users_id], backref="users_grant", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())