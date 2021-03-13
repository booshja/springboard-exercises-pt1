"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """
        Create test client, add sample data.
        """

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """
        Does basic model work?
        """

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_method(self):
        """
        Checks the repr method works as expected
        """
        user = User(email="test@test.com", username="testuser",
                    password="HASHED_PASSWORD")
        db.session.add(user)
        db.session.commit()
        db_user = User.query.filter_by(username='testuser').first()

        self.assertEqual(
            str(user), f"<User id={db_user.id} username={db_user.username} email={db_user.email}>")

    def test_user1_following_user2(self):
        """
        TESTS:
        - is_following successfully detects when user1 is following user2
        - is_following successfully detects when user2 is not follwing user1
        """
        user_1 = User(email="test@test.com", username="testuser",
                      password="HASHED_PASSWORD")
        user_2 = User(email="krew@test.com", username="testkrew",
                      password="KREW_HASHED_PASSWORD")
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

        user1 = User.query.filter_by(username="testuser").first()
        user2 = User.query.filter_by(username="testkrew").first()

        new_follow = Follows(user_being_followed_id=user2.id,
                             user_following_id=user1.id)

        db.session.add(new_follow)
        db.session.commit()

        follow = Follows.query.filter_by(
            user_being_followed_id=user2.id).first()

        self.assertEqual(user1.is_following(user2), True)
        self.assertEqual(user2.is_following(user1), False)

    def test_user2_following_user1(self):
        """
            TESTS:
            - is_following successfully detects when user2 is following user1
            - is_following successfully detects when user1 is not follwing user2
            """
        user_1 = User(email="test@test.com", username="testuser",
                      password="HASHED_PASSWORD")
        user_2 = User(email="krew@test.com", username="testkrew",
                      password="KREW_HASHED_PASSWORD")
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

        user1 = User.query.filter_by(username="testuser").first()
        user2 = User.query.filter_by(username="testkrew").first()

        new_follow = Follows(user_being_followed_id=user1.id,
                             user_following_id=user2.id)

        db.session.add(new_follow)
        db.session.commit()

        follow = Follows.query.filter_by(
            user_being_followed_id=user2.id).first()

        self.assertEqual(user2.is_following(user1), True)
        self.assertEqual(user1.is_following(user2), False)


# Does User.create successfully create a new user given valid credentials?
# Does User.create fail to create a new user if any of the validations(e.g. uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?
