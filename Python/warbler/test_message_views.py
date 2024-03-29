"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


from app import app, CURR_USER_KEY
from unittest import TestCase
from models import db, Message, User

app.config['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """
    Test views for messages.
    """

    def setUp(self):
        """
        Create test client, add sample data.
        """

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def fake_login(self, client):
        """
        Setting up fake login via changing-session trick
        """
        with client.session_transaction() as sess:
            sess[CURR_USER_KEY] = self.testuser.id

    def test_add_message(self):
        """
        TESTS:
        Can use add a message?
        """

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            self.fake_login(c)

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_show_message(self):
        """
        TESTS:
        - Correct response code
        - Does the page display the message?
        """
        with self.client as client:
            self.fake_login(client)

            msg = client.post("/messages/new",
                              data={"text": "testing...testing"})
            message = Message.query.one()

            resp = client.get(f'/messages/{message.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testing...testing", html)

    def test_destroy_message(self):
        """
        TESTS:
        - Correct response code
        - Does the message get deleted?
        """
        with self.client as client:
            self.fake_login(client)

            msg = client.post("/messages/new",
                              data={"text": "testing...testing"})
            message = Message.query.one()

            resp = client.post(f'/messages/{message.id}/delete')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(len(Message.query.all()), 0)
