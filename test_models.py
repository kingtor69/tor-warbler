# starter code by Colt Steele and/or Rithm School and/or Springboard
# Tor Kingdon added liberally (as noted)
"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

# additional models added by Tor Kingdon
from models import db, User, Message, Follow, Like
from datetime import datetime

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

# invalid postgres name (with a dash) changed by Tor Kingdon
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for users."""

# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follow.query.delete()

        self.client = app.test_client()

    # teardown created by Tor Kingdon
    def tearDown(self):
        """get rid of any fragments created by flawed tests"""        
        db.session.rollback()

    def test_user_model(self):
        # detailed docstring by Tor Kingdon
        """Does basic User model work?
        A new user should:
            - exist (any test referring to it will fail if it does not exist)
            - have zero messages and zero followers
            - should have a hashed password, i.e:
                - password in database should *not* equal the entered password
                - hashed password should have a length of 60 characters
                - all Bcrypt strings start with '$2b$'
        User.__repr__(u) should return correct information
        """
        # user definition rewritten (to include password hashing) by Tor Kingdon
        u = User.signup("test_user", "test@test.com", "UNHASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        # password hashing tests written by Tor Kingdon
        self.assertNotEqual(u.password, "UNHASHED_PASSWORD")
        self.assertEqual(len(u.password), 60)
        self.assertTrue(u.password.startswith("$2b$"))
        # __repr__ test written by Tor Kingdon
        self.assertEqual(u.__repr__(), f"<User #{u.id}: {u.username}, {u.email}>")

    # exceptions tests written by Tor Kingdon
    # with a hint taken from the solution code by Colt Steele and/or Rithm School and/or Springboard
    def test_incomplete_user_exception(self):
        """Test if imcomplete data yields a TypeError."""
        u_username_only = User(username="incomplete_user")
        with self.assertRaises(TypeError) as err:
            User.signup(u_username_only)

    def test_invalid_password(self):
        """TypeError should result if password is under 6 characters in length"""
        u_invalid_password = User(username="bad_user", email="bad@baduser.com", password="df")
        with self.assertRaises(TypeError) as err:
            User.signup(u_invalid_password)

    # authentication tests written by Tor Kingdon
    def test_user_authentication(self):
        """test User.authenitcate(), which should:
            - return a user when sent valid credentials
            - return False when sent invalid username
            - return False when sent invalid password
        """
        u = User.signup("testuser", "test@email.com", "hashedPotat03$", None, None, None, None)
        
        self.assertEqual(User.authenticate("testuser", "hashedPotat03$"), u)
        self.assertEqual(User.authenticate("testyuser", "hashedPotat03$"), False)
        self.assertEqual(User.authenticate("testuser", "smashedPotat03$"), False)

# rest of model test cases written by Tor Kingdon
class MessageModelTestCase(TestCase):
    """Test model for messages."""

    def setUp(self):
        """clear data from pertinent models, and set up test_client."""

        User.query.delete()
        Message.query.delete()
        Like.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """get rid of any fragments created by flawed tests"""        
        db.session.rollback()

    def test_message_model(self):
        """Does basic Message model work?
        A new message should:
            - exist (any test referring to it will fail if it does not exist)
            - have a valid datetime time stamp
            - have zero likes
            - return posting user's id from the user_id column
        """

        ### no need to take the time to salt & hash password for this test
        u = User(
                 username = "test_user",
                 email = "test@test.com",
                 password = "HASHED_PASSWORD"    
            )
        db.session.add(u)
        db.session.commit()

        m = Message(text="warble warble", user_id=u.id)

        u.messages.append(m)
        db.session.commit()

        self.assertNotIn(m.id, Like.query.all())
        self.assertTrue(m.timestamp.today)
        self.assertEqual(m.user_id, u.id)
        self.assertEqual(m.__repr__(), f"<Message #{m.id}: {m.text}, {u.username}>")


class FollowModelTestCase(TestCase):
    """Test model for Follow"""

    def setup(self):
        """clear data from pertinent models, and set up test_client."""
        User.query.delete()
        Follow.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """get rid of any fragments created by flawed tests"""
        db.session.rollback()

    def test_follow_model(self):
        """Does basic Follow model work?
        A new follow row should:
            - exist (any test referring to it will fail if it does not exist)
            - return u1 as follower and u2 as followee
            - not return the opposite (specific to test case, not necessarily true in production)
            - return u2 as being followed by u1
            - not return the opposite (again, specific to test case)
        """
        ### no need to take the time to salt & hash password for this test
        u1 = User(
                 username = "test_user1",
                 email = "test1@test.com",
                 password = "HASHED_PASSWORD1"    
            )
        u2 = User(
                 username = "test_user2",
                 email = "test2@test.com",
                 password = "HASHED_PASSWORD2"    
            )
    

        db.session.add_all([u1, u2])
        db.session.commit()
        f = Follow(user_being_followed_id=u2.id, user_following_id=u1.id)
        db.session.add(f)
        db.session.commit()
        all_follows = Follow.query.all()

        self.assertEqual(f.user_being_followed_id, u2.id)
        self.assertEqual(f.user_following_id, u1.id)
        for follow in all_follows:
            self.assertNotEqual(u1.id, follow.user_being_followed_id)
            self.assertNotEqual(u2.id, follow.user_following_id)

class LikeModelTestCase(TestCase):
    """Test model for Follow"""

    def setup(self):
        """clear data from pertinent models, and set up test_client."""

        User.query.delete()
        Message.query.delete()
        Like.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """get rid of any fragments created by flawed tests"""
        db.session.rollback()

    def test_like_model(self):
        """test basic like model
        A new like should:
            - refer to the liking user
            - refer to the liked message
        """
        u = User(
                 username = "like_test_user",
                 email = "liketest@test.com",
                 password = "HASHED_POTATOES"    
            )

        db.session.add(u)
        db.session.commit()

        m = Message(text="warble warble", user_id=u.id)

        u.messages.append(m)
        db.session.commit()

        l = Like(user_id=u.id, message_id=m.id)

        db.session.add(l)
        db.session.commit()

        self.assertEqual(l.user_id, u.id)
        self.assertEqual(l.message_id, m.id)