from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTestCase(TestCase):
    """Tests for Flask"""

    def setUp(self):
        """Add sample user"""
        User.query.delete()

        user = User(first_name="John", last_name="Johnson",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png")
        self.user_id = user.id

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Clean up any leftover commits"""
        db.session.rollback()

    def test_home_page_redirect(self):
        """
        TESTS:
        -Home page redirects to the /users page by default
        """
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)

    def test_list_users(self):
        """
        TESTS:
        -Page is displayed with correct status code
        -User is displayed on the page
        """
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Johnson', html)

    def test_add_new_user_page_display(self):
        """
        TESTS:
        -Page is displayed with correct status code
        -Form is correctly displayed
        """
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<button type="submit" class="btn btn-success">Add</button>', html)

    def test_new_user_added(self):
        """
        TESTS:
        -Adds new user
        -Displayed on user list page
        """
        data = {"first_name": "Jacob", "last_name": "Andes",
                "image_url": "https://comotion.uw.edu/wp-content/uploads/2019/05/generic-profile.png"}
        with app.test_client() as client:
            resp = client.post('/users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jacob Andes", html)

    def test_user_detail_page_display(self):
        """
        TESTS:
        -Page is displayed with correct status code
        -User detail card is displayed
        """
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Johnson", html)

    def test_users_edit_page(self):
        """
        TESTS:
        -Page is displayed with correct status code
        -User details are auto-filled in inputs
        """
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('value="Johnson"', html)

    def test_delete_user(self):
        """
        TESTS:
        -Page is displayed with correct status code
        -The user has been deleted from the user list
        """
        with app.test_client() as client:
            resp = client.post(
                f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("John Johnson", html)

    def test_new_post_page(self):
        """
        TESTS:
        -Page is displayed with correct status code
        """
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                ' <label for="content-field">Content: </label>', html)

    def test_new_post_execution(self):
        """
        TESTS:
        -Page is displayed with correct status code
        -New story submitted is in list of stories
        """
        data = {"title": "I love dogs",
                "content": "They're so great aren't they? Plus they're real cute and fun to have around. It's always interesting!"}
        with app.test_client() as client:
            resp = client.post(
                f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("I love dogs", html)
