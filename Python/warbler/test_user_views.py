"""User View tests."""

import os
from app import app, CURR_USER_KEY
from unittest import TestCase
from models import db, Message, User, Follows

app.config['TESTING'] = True

db.create_all()

app.config['WTF_CSRE_ENABLED'] = False


class UserViewTestCase(TestCase):
    """
    Test views for users.
    """

    def setUp(self):
        """
        create test client, add sample data
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

    def test_homepage_anon(self):
        """
        TESTS:
        - Status code returns correct
        - Anon user: no messages
        """
        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>What's Happening?</h1>", html)

    def test_homepage_user(self):
        """
        TESTS:
        - Status code returns correct
        - Messages are displayed
        """
        with self.client as client:
            self.fake_login(client)

            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Warble", html)

    def test_list_users(self):
        """
        TESTS:
        - Status code returns correct
        - testuser is displayed as the only user
        """
        with self.client as client:
            self.fake_login(client)

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@testuser</p>", html)

    def test_users_show(self):
        """
        TESTS:
        - Status code returns correct
        - testuser profile is displayed correctly
        """
        with self.client as client:
            self.fake_login(client)

            resp = client.get(f'/users/{self.testuser.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4 id="sidebar-username">@testuser</h4>', html)

    def test_show_following(self):
        """
        TESTS:
        - Status code comes correct
        - The user being followed shows up on the page
        """
        with self.client as client:
            self.fake_login(client)

            test = User.signup(
                username="ralph", email="ralph@email.com", password="HASHED_PASSWORD", image_url=None)
            db.session.commit()

            ralph = User.query.filter_by(username="ralph").first()

            new_follow = Follows(
                user_being_followed_id=ralph.id, user_following_id=self.testuser.id)
            db.session.add(new_follow)
            db.session.commit()

            resp = client.get(f'/users/{self.testuser.id}/following')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>@ralph</p>', html)

    def test_users_followers(self):
        """
        TESTS:
        - Status code returns correct
        - The user following shows up on the page
        """
        with self.client as client:
            self.fake_login(client)

            test = User.signup(
                username="ralph", email="ralph@email.com", password="HASHED_PASSWORD", image_url=None)
            db.session.commit()

            ralph = User.query.filter_by(username="ralph").first()

            new_follow = Follows(
                user_being_followed_id=self.testuser.id, user_following_id=ralph.id)
            db.session.add(new_follow)
            db.session.commit()

            resp = client.get(f'/users/{self.testuser.id}/followers')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>@ralph</p>', html)

    def test_add_follow(self):
        """
        TESTS:
        - Status code returns correct (redirect)
        - Follower is added to the page
        """
        with self.client as client:
            self.fake_login(client)

            test = User.signup(username="ralph", email="ralph@email",
                               password="HASHED_PASSWORD", image_url=None)
            db.session.commit()

            ralph = User.query.filter_by(username="ralph").first()

            resp = client.post(
                f'/users/follow/{ralph.id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@ralph</p>", html)

    def test_stop_following(self):
        """
        TESTS:
        - Status code returns correct
        - Follower is removed from the page
        """
        with self.client as client:
            self.fake_login(client)

            test = User.signup(username="ralph", email="ralph@email",
                               password="HASHED_PASSWORD", image_url=None)
            db.session.commit()

            ralph = User.query.filter_by(username="ralph").first()

            new_follow = Follows(
                user_being_followed_id=ralph.id, user_following_id=self.testuser.id)
            db.session.add(new_follow)
            db.session.commit()

            resp = client.post(
                f'/users/stop-following/{ralph.id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("<p>@ralph</p>", html)

    def test_profile(self):
        """
        TESTS:
        -
        """

    def test_destroy_user(self):
        """
        TESTS:
        -
        """

    def test_add_like(self):
        """
        TESTS:
        -
        """

    def test_remove_like(self):
        """
        TESTS:
        -
        """

    def test_show_likes(self):
        """
        TESTS:
        -
        """
