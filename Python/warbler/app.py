from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, User, Message, Likes, Follows

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI', 'postgres:///warbler-test')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

CURR_USER_KEY = os.environ.get('CURR_USER_KEY')

toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """
    If we're logged in, add curr user to Flask global.
    """

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """
    Log in user.
    """

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    GET ROUTE:
    - Display signup form
    ----------
    POST ROUTE:
    Handle user signup.
    - Create new user and add to DB.
    - Redirect to home page.
    - If form not valid, present form.
    - If the there already is a user with that username: flash message and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    GET ROUTE:
    - Display login form
    ----------
    POST ROUTE:
    - Handle user login.
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """
    GET ROUTE:
    - Handle logout of user.
    """

    do_logout()

    flash("Logout successful.", "info")

    return redirect('/login')


##############################################################################
# General user routes:

@app.route('/users')
def list_users():
    """
    GET ROUTE:
    - Page with listing of users.
    - Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """
    GET ROUTE:
    - Show user profile.
    """

    user = User.query.get_or_404(user_id)

    # snagging messages in order from the database;
    # user.messages won't be in order by default
    messages = (Message
                .query
                .filter(Message.user_id == user_id)
                .order_by(Message.timestamp.desc())
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, messages=messages)


@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """
    GET ROUTE:
    - Show list of people this user is following.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """
    GET ROUTE:
    - Show list of followers of this user.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)


@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """
    POST ROUTE:
    - Add a follow for the currently-logged-in user.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """
    POST ROUTE:
    - Have currently-logged-in-user stop following this user.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@app.route('/users/profile/<int:user_id>', methods=["GET", "POST"])
def profile(user_id):
    """
    GET ROUTE:
    - Show form with pre-filled data
    ----------
    POST ROUTE:
    -Update profile for current user.
    """

    form = UserEditForm()
    user = User.query.get_or_404(user_id)

    if user.id != session[CURR_USER_KEY]:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    if form.validate_on_submit():
        pwd = form.password.data

        if User.authenticate(user.username, pwd):
            user.username = form.username.data or user.username
            user.email = form.email.data or user.email
            user.image_url = form.image_url.data or user.image_url
            user.header_image_url = form.header_image_url.data or user.header_image_url
            user.bio = form.bio.data or user.bio
            user.location = form.location.data or user.location

            db.session.add(user)
            db.session.commit()

            flash("Profile updated!", "success")
            return redirect(f'/users/{user.id}')
        else:
            flash("Incorrect password", "danger")
            return redirect(f'/users/profile/{user.id}')
    else:
        form.username.data = user.username
        form.email.data = user.email
        form.image_url.data = user.image_url
        form.header_image_url.data = user.header_image_url
        form.bio.data = user.bio
        form.location.data = user.location
        return render_template('/users/edit.html', form=form, user=user)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """
    POST ROUTE:
    - Delete user.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    flash("User deleted.", "info")

    return redirect("/signup")


##############################################################################
# Messages routes:

@app.route('/messages/new', methods=["GET", "POST"])
def messages_add():
    """
    GET ROUTE:
    - Show form
    ----------
    POST ROUTE:
    Add a message:
    - If valid, update message and redirect to user page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(text=form.text.data)
        g.user.messages.append(msg)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('messages/new.html', form=form)


@app.route('/messages/<int:message_id>', methods=["GET"])
def messages_show(message_id):
    """
    GET ROUTE:
    - Show a message.
    """

    msg = Message.query.get(message_id)
    return render_template('messages/show.html', message=msg)


@app.route('/messages/<int:message_id>/delete', methods=["POST"])
def messages_destroy(message_id):
    """
    POST ROUTE:
    - Delete a message.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    msg = Message.query.get(message_id)
    db.session.delete(msg)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


##############################################################################
# Likes processing routes:


@app.route('/users/add_like/<int:msg_id>', methods=["POST"])
def add_like(msg_id):
    """
    POST ROUTE:
    - Process adding a like to a warble for the user
    """

    if g.user:
        user = User.query.get_or_404(g.user.id)
        like = Likes(user_id=user.id, message_id=msg_id)

        db.session.add(like)
        db.session.commit()

        flash("Warble liked!", "success")
        return redirect('/')
    else:
        flash("You must be logged in to do this!", "danger")
        return redirect('/login')


@app.route('/users/remove_like/<int:msg_id>', methods=["POST"])
def remove_like(msg_id):
    """
    POST ROUTE:
    - Process removing a like from a warble for the user
    """

    if g.user:
        user = User.query.get_or_404(g.user.id)
        like = Likes.query.filter_by(
            message_id=msg_id, user_id=user.id).first()

        db.session.delete(like)
        db.session.commit()

        flash("Like removed.", "info")
        return redirect('/')


@app.route('/users/<int:user_id>/likes')
def show_likes(user_id):
    """
    GET ROUTE:
    - Show all the messages the user has liked
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    user = User.query.get_or_404(user_id)
    return render_template('/users/likes.html', user=user)
##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """
    GET ROUTE:
    Show homepage:
    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        user = User.query.get_or_404(g.user.id)
        following_ids = [u.id for u in user.following]
        following_ids.append(user.id)
        messages = (Message
                    .query
                    .order_by(Message.timestamp.desc())
                    .filter(Message.user_id.in_(following_ids))
                    .limit(100)
                    .all())
        likes = user.likes

        return render_template('home.html', messages=messages, likes=likes)

    else:
        return render_template('home-anon.html')


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """
    Add non-caching headers on every request.
    """

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
