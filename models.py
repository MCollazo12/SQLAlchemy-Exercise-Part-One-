from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        """Show info about a user."""

        u = self
        return f"<User {u.id} First Name: {u.first_name} Last Name: {u.last_name} Image URL: {u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    image_url = db.Column(db.VARCHAR(2048), nullable=False, unique=False)
    
    posts = db.relationship('Post', backref='user')

    @classmethod
    def get_user(cls, user_id):
        """Get user matching a certain id."""

        return cls.query.filter_by(id=user_id).first()

    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"




class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    user_key = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def get_timestamp(self):
        """Get the post's timestamp"""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")