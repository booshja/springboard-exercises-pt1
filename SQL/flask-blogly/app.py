"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretchickenz'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """GET ROUTE:
    -Redirects to the /users page by default"""
    return redirect('/users')


@app.route('/users')
def users_list_page():
    """
    GET ROUTE:
    -Show all users as links to view detail page for user, link to add user form
    """
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users or None)


@app.route('/users/new')
def add_new_user_page():
    """GET ROUTE:
    -Shows a form to add a user, posts to /users/new
    """
    return render_template('new-user.html')


@app.route('/users/new', methods=["POST"])
def process_new_user():
    """
    POST ROUTE:
    -Processes the add form, adding new user and returning to /users
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """
    GET ROUTE:
    -Show info about given user
    """
    user = User.query.get_or_404(user_id)

    return render_template('user-detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_details(user_id):
    """
    GET ROUTE:
    -Shows the edit page for given user
    """
    user = User.query.get_or_404(user_id)

    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_user_edit(user_id):
    """
    POST ROUTE:
    -process edit form, returning user to /users page
    """
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']

    if request.form['image_url'] == "":
        user.image_url = User.default_img_url()
    else:
        user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """
    POST ROUTE:
    -Process deletion of given user, returning user to /users page
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
