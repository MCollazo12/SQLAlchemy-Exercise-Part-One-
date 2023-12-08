from app import app
from models import db
from unittest import TestCase


class AppTestCase(TestCase):
    def setUp(self):
        """Set up the test environment."""
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_redirect_users(self):
        """Test the / route redirects to /users."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/users")

    def test_list_users(self):
        """Test the /users route returns a 200 status code."""
        response = self.app.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_add_new_user(self):
        """Test adding a new user."""
        data = {
            "first_name": "Michael",
            "last_name": "Collazo",
            "image_url": "https://example.com/image.jpg",
        }
        response = self.app.post("/users/new", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Michael Collazo", response.data)
        self.assertIn(b"User added successfully!", response.data)

    def test_add_new_user_missing_fields(self):
        """Test adding a new user with missing fields."""
        data = {
            "first_name": "",
            "last_name": "",
            "image_url": "https://example.com/image.jpg",
        }
        response = self.app.post("/users/new", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"First name and last name are required.", response.data)
