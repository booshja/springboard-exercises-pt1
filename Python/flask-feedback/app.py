from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from secrets import SECRET_KEY
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
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
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            flash(f'Logged in! Welcome back, {user.username}!')
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username or password']

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    """
    GET ROUTE:
    -Display information about the user
    """
    if 'username' not in session:
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        return render_template('user-detail.html', user=user)

    return "<h1 class='display-1'>You made it!</h1>"


@app.route('/logout')
def logout_user():
    """
    GET ROUTE:
    -Logout the user (clear the session)
    -Redirect to /
    """
    session.pop('username')
    return redirect('/')
