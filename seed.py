from models import User, Post, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    u1 = User(first_name='', last_name='' ,image_url='')
    u2 = User(first_name='', last_name='' ,image_url='')
    p1 = Post(title='', content='', created_at='', user_key='')
    p1 = Post(title='', content='', created_at='', user_key='')

    db.session_add_all(u1, u2)