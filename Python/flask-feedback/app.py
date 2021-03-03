from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from secrets import SECRET_KEY
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
# from sqlalchemy.exc import

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """
    GET ROUTE:
    -Redirects to /register
    """
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """
    GET ROUTE:
    -Show a form that when submitted will register/create a user
    -This form should accept a username, password, email, first_name
        and last_name
    ===================================================
    POST ROUTE:
    -Process the registration form by adding a new user
    -Redirect to /users/<username>
    """
    if 'username' in session:
        username = session['username']
        return redirect(f'/users/{username}')
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.username.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            new_user = User.register(
                username, password, email, first_name, last_name)
            db.session.add(new_user)
            db.session.commit()

            session['username'] = new_user.username
            flash('New user registered!', 'info')
            return redirect(f'/users/{new_user.username}')

        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
    GET ROUTE:
    -Show a form that when submitted will login a user
    -This form should accept a username and a password.
    ===================================================
    POST ROUTE:
    -Process the login form
    -Ensure the user is authenticated
        -If so, redirect to /users/<username>
    """
    if 'username' in session:
        username = session['username']
        flash("You're already logged in!", 'info')
        return redirect(f'/users/{username}')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.authenticate(username, password)

            if user:
                session['username'] = user.username
                flash(f'Logged in! Welcome back, {user.username}!', 'success')
                return redirect(f'/users/{user.username}')
            else:
                form.username.errors = ['Invalid username or password']

        return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    """
    GET ROUTE:
    -Display information about the user
    -Show all of the feedback that the user has given
    -For each piece of feedback, display with a link to a rom
        to edit the feedback and a button to delete the feedback
    -Have a link that sends you to a form to add more feedback
        and a button to delete the user.
    """
    if 'username' not in session:
        flash("Ooops that's not you!", 'info')
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        feedback = user.feedbacks
        return render_template('user-detail.html', user=user, feedback=feedback, username=username)


@app.route('/logout')
def logout_user():
    """
    GET ROUTE:
    -Logout the user (clear the session)
    -Redirect to /
    """
    session.pop('username')
    flash("You have been logged out.", 'info')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """
    GET ROUTE:
    -Display a form to add feedback
    POST ROUTE:
    -Add a new pice of feedback
    -Redirect to /users/<username>
    """
    if 'username' in session:
        form = FeedbackForm()

        if form.validate_on_submit():
            user = User.query.get_or_404(username)
            title = form.title.data
            content = form.content.data
            new_feed = Feedback(title=title, content=content,
                                username=user.username)
            db.session.add(new_feed)
            db.session.commit()
            flash('Feedback created!', 'success')
            return redirect(f'/users/{user.username}')
        else:
            return render_template('add-feedback.html', form=form, username=username)
    else:
        return redirect('/login')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """
    POST ROUTE:
    -Remove the user from the database
        -Also removes all of the user's feedback
    -Clear any user information in the session
    -Redirect to '/'
    """
    if 'username' in session:
        if session['username'] == username:
            user = User.query.get_or_404(username)
            feedbacks = Feedback.query.filter(username == user.username)
            for feed in feedbacks:
                db.session.delete(feed)
            db.session.delete(user)
            db.session.commit()
            session.pop('username')
            flash('User deleted.', 'success')
            return redirect('/')
        else:
            flash("You cannot delete other users.", 'danger')
            return redirect(f'/users/{username}')
    else:
        flash("You do not have permission to do this!", 'danger')
        return redirect('/')


@app.route('/feedback/<feed_id>/delete', methods=['POST'])
def delete_feedback(feed_id):
    """
    POST ROUTE:
    -Delete a piece of feedback
    -Redirect to '/users/<username>'
    """
    if 'username' in session:
        feedback = Feedback.query.get_or_404(feed_id)
        if session['username'] == feedback.username:
            db.session.delete(feedback)
            db.session.commit()
            flash('Feedback deleted.', 'success')
            return redirect(f"/users/{session['username']}")

        else:
            flash("You cannot delete other users' feedback!", 'danger')
            return redirect(f"/users/{session['username']}")
    else:
        flash('You do not have permission to do this!', 'danger')
        return redirect('/register')


@app.route('/feedback/<feed_id>/update', methods=['GET', 'POST'])
def update_feedback(feed_id):
    """
    GET ROUTE:
    -Display a form to edit feedback
    POST ROUTE:
    -Update a specific piece of feedback
    -Redirect to '/users/<username>'
    """
    if 'username' in session:
        feedback = Feedback.query.get_or_404(feed_id)
        if session['username'] == feedback.username:
            form = FeedbackForm()

            if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data
                db.session.commit()
                flash('Feedback updated!', 'info')
                return redirect(f"/users/{feedback.username}")

            form.title.data = feedback.title
            form.content.data = feedback.content
            return render_template('update-feedback.html', form=form, username=feedback.username)
        else:
            flash("You cannot edit other users' feedback!", 'danger')
            return redirect(f"/users/{session['username']}")
    else:
        flash('You do not have permission to do this!', 'danger')
        return redirect('/register')
