from config import db
from sqlalchemy.sql import func

likes_ideas_table = db.Table('ideas_likes',
    db.Column(
        'idea_id',
        db.Integer,db.ForeignKey(
            'ideas.id',
            ondelete="cascade"
        ),
        primary_key=True
    ),
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'created_at',
        db.DateTime,
        server_default=func.now()
    )
)