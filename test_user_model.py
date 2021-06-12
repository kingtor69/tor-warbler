"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follow, Like
from datetime import datetime

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follow.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Does basic User model work?
        A new user should:
            - exist
            - have zero messages and zero followers
            - should have a hashed password, i.e:
                - password in database should *not* equal the entered password
                - hashed password should have a length of 60 characters
        """
        u = User.signup("test_user", "test@test.com", "HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertNotEqual(u.password, "HASHED_PASSWORD")
        self.assertEqual(len(u.password), 60)

class MessageModelTestase(TestCase):
    """Test model for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follow.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Does basic Message model work?
        A new message should:
            - exist
            - have a time stamp
            - have zero likes
        """
        u = User.signup("test_user", "test@test.com", "HASHED_PASSWORD")
        m = Message(text="warble warble")

        u.messages.append(m)
        db.session.commit()

        self.assertNotIn(m.id, Like.query.all())
        self.assertIs(m.datetime, datetime.datetime)
