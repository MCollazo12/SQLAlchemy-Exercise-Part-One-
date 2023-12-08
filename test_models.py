from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import db, User
from unittest import TestCase


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False


class TestUserModel(TestCase):
    """User model tests"""

    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.drop_all()
            db.create_all()

    @classmethod
    def tearDown(cls):
        """Rolls back a transaction"""
        with app.app_context():
            db.session.rollback()
            db.session.close()
            db.drop_all()

    def setUp(self):
        """Cleans up any existing users in the database"""
        with app.app_context():
            User.query.delete()

    def test_user_creation(self):
        """Test the creation of a new user"""
        with app.app_context():
            user = User(
                first_name="Michael", last_name="Collazo", image_url="example.jpg"
            )
            db.session.add(user)
            db.session.commit()

            # Retrieve the user from the database
            retrieved_user = User.query.get(user.id)

            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.first_name, "Michael")
            self.assertEqual(retrieved_user.last_name, "Collazo")
            self.assertEqual(retrieved_user.image_url, "example.jpg")

    def test_get_user(self):
        """Test the retrieval of a user using the 'get_user' class method"""

        with app.app_context():
            user = User(
                id=1, first_name="Michael", last_name="Collazo", image_url="example.jpg"
            )
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.get_user(1)
            self.assertEqual(user, retrieved_user)
