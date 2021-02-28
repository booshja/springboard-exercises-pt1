from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Dog_silhouette.svg/1200px-Dog_silhouette.svg.png'


def connect_db(app):
    """Connects and initializes the database for the app"""
    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """A pet potentially available for adoption"""

    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)

    @classmethod
    def check_url(input_url):
        """Check to see if the URL is None, if so, return default url"""

        if input_url == None:
            return DEFAULT_IMAGE_URL
        else:
            return input_url
