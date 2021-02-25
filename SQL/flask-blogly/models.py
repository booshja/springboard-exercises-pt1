"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
DEFAULT_IMG_URL = 'https://comotion.uw.edu/wp-content/uploads/2019/05/generic-profile.png'


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(
        db.Text, nullable=False, default=DEFAULT_IMG_URL)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

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
        """Creates a better readable display of the User instance"""
        p = self
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"


class Post(db.Model):
    """Posts by users model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='posts_tags',
                           cascade='all, delete', backref='posts')

    def __repr__(self):
        """Creates a better readable display of the Post instance"""
        p = self
        return f'<Post id={p.id} title={p.title} created_at={p.created_at} user_id={p.user_id}'


class PostTag(db.Model):
    """Join Table for Post and Tag"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tags for posts"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        """Creates a better readable display of the Tag instance"""
        t = self
        return f'<Tag id={t.id} name={t.name}>'
