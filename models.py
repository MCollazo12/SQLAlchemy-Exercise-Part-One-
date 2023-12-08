"""Demo file showing off a model for SQLAlchemy."""
from flask_sqlalchemy import SQLAlchemy

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

    @classmethod
    def get_user(cls, user_id):
        """Get user matching a certain id."""

        return cls.query.filter_by(id=user_id).first()
