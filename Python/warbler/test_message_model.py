"""Message model tests."""

from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()


class MessageModelTestCase(TestCase):
    """Test models for messages"""

    def setUp(self):
        """
        Clean up User, Message data
        """
        User.query.delete()
        Message.query.delete()

    def tearDown(self):
        """
        Clean up any fouled transactions
        """
        db.session.rollback()

    def test_message_model(self):
        """
        TESTS:
        - Does basic model work?
        """
        db.session.add(
            User(username="krew", email="krew@email.com", password="HASHED_PASSWORD"))
        db.session.commit()
        user = User.query.filter_by(username="krew").first()

        new_message = Message(text="This is a test.", user_id=user.id)
        db.session.add(new_message)
        db.session.commit()
        message = Message.query.filter_by(user_id=user.id).first()

        self.assertEqual(message.text, "This is a test.")
        self.assertEqual(message.user_id, user.id)

    def test_repr_method(self):
        """
        TESTS:
        - repr method works as expected
        """
        db.session.add(
            User(username="krew", email="krew@email.com", password="HASHED_PASSWORD"))
        db.session.commit()
        user = User.query.filter_by(username="krew").first()

        new_message = Message(text="This is a test.", user_id=user.id)
        db.session.add(new_message)
        db.session.commit()
        message = Message.query.filter_by(user_id=user.id).first()

        self.assertEqual(str(
            message), f'<Message id={message.id} text={message.text} timestamp={message.timestamp} user_id={message.user_id}>')

    def message_create_failure(self):
        """
        TESTS:
        -
        """
        error = False

        message = Message(text="Oopsie!")
        db.session.add(message)
        try:
            db.session.commit()
        except:
            error = True

        self.assertEqual(error, True)
