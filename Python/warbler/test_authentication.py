"""User authentication view tests."""

from app import app, CURR_USER_KEY
from unittest import TestCase

from models import db, Message, User

app.config['DATABASE_URI'] = 'postgresql:///warbler-test'
app.config['TESTING'] = True

db.create_all()

app.config['WTF_CSRE_ENABLED'] = False


class UserAuthenticationTestCase(TestCase):
    """
    Test views for user authentication and authorization
    """

    def setUp(self):
        """
        create test client, add sample data
        """

        User.query.delete()

        self.client = app.test_client()
