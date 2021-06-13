# written entirely by Tor Kingdon

import os
from unittest import TestCase

# use testing database -- from starter code in test_models_users.py by Colt Steele and/or Rithm School and/or Springboard, except as noted

# additional models added by Tor Kingdon
from models import db, User, Message, Follow, Like
from datetime import datetime

# invalid postgres name (with a dash) changed by Tor Kingdon
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"
### end of starter code ###

from app import app
from flask import session, g

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# reset database
db.create_all()

class NoUserTestCase(TestCase):
    """Testing various routes with no user logged in."""

    def setUp(self):
        User.query.delete()
        Message.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_landing_page_no_user(self):
        """Tests landing page for user not logged in. 
        should show sign-up button"""
        
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/signup" class="btn btn-primary">Sign up</a>', html)

    def test_new_user_signup_form(self):
        """Test new user registration form."""

        with app.test_client() as client:
            resp = client.get('/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button class="btn btn-primary btn-lg btn-block">Sign me up!</button>', html)

    def test_manual_navigation_to_users_no_logged_in_user(self):
        """All users can be viewed whether logged in or not. Test to see if this is working with manual navaigation to users index page."""

        # prepopulate database with test user:
        u1 = User(
                username = "test_user1",
                email = "test1@test.com",
                password = "HASHED_PASSWORD1"    
            )
        db.session.add(u1)
        db.session.commit()
        
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            expected_html_anchor = f'<a href="/users/{u1.id}" class="card-link">'
            expected_html_img = f'<img src="/static/images/default-pic.png" alt="Image for {u1.username}" class="card-image">'

            self.assertEqual(resp.status_code, 200)
            self.assertIn(expected_html_anchor, html)
            self.assertIn(expected_html_img, html)
            
    def test_manual_navigation_to_user_profile_no_logged_in_user(self):
        """All users can be viewed whether logged in or not. Test to see if test user's profile page can be viewed without being logged in."""

        # prepopulate database with test user and message:
        u1 = User(
                username = "test_user1",
                email = "test1@test.com",
                password = "HASHED_PASSWORD1"    
            )
        db.session.add(u1)
        db.session.commit()
        
        m = Message(text="warble warble", user_id=u1.id)

        u1.messages.append(m)
        db.session.commit()

        with app.test_client() as client:
            resp = client.get(f'/users/{u1.id}')
            html = resp.get_data(as_text=True)

            expected_html_username = f'<h4 id="sidebar-username" class="card-header">@{u1.username}</h4>'
            expected_html_warble_text = f'<p>{m.text}</p>'

            self.assertEqual(resp.status_code, 200)
            self.assertIn(expected_html_username, html)
            self.assertIn(expected_html_warble_text, html)
            
