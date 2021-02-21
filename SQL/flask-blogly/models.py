"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMG_URL = 'https://comotion.uw.edu/wp-content/uploads/2019/05/generic-profile.png'


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(
        db.Text, nullable=False, default=DEFAULT_IMG_URL)

    @classmethod
    def default_img_url(self):
        """Returns default image url"""
        return DEFAULT_IMG_URL

    @classmethod
    def get_all_users(cls):
        """Returns all the users from the database"""
        return cls.query.all()

    @property
    def full_name(self):
        """Returns user's full name"""
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        """Shows a human-redable representation of the User instance"""
        p = self
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"
