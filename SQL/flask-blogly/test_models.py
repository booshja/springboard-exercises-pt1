from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users"""

    def setUp(self):
        """Clean up any existing users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_default_img_url(self):
        """Test that class returns proper default img url"""
        user = User(first_name="John", last_name="Johnson",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png")
        self.assertEquals(User.default_img_url(
        ), 'https://comotion.uw.edu/wp-content/uploads/2019/05/generic-profile.png')

    def test_full_name(self):
        """Test that full name property is correct when user being created"""
        user = User(first_name="John", last_name="Johnson",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png")
        self.assertEquals(user.full_name, 'John Johnson')

    def test_attributes(self):
        """Test that attributes are correctly returned when user is created"""
        user = User(first_name="John", last_name="Johnson",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png")
        self.assertEquals(user.first_name, "John")
        self.assertEquals(user.last_name, "Johnson")
        self.assertEquals(
            user.image_url, "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png")

    def test_get_all_users(self):
        """Test to make sure get all users is functioning correctly"""
        user_john = User(first_name="John", last_name="Johnson",
                         image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png")
        db.session.add(user_john)
        db.session.commit()

        users_list = User.get_all_users()
        self.assertEquals(users_list, [user_john])
