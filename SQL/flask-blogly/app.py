"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretchickenz'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """GET ROUTE:
    -Redirects to the /users page by default"""
    return redirect('/users')


############################################################
# ----------USERS ROUTES---------- #
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
    -Show any posts the user has created in a list
    """
    user = User.query.get_or_404(user_id)
    posts = Post.query.all()

    return render_template('user-detail.html', user=user, posts=posts or None)


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

############################################################
# ----------POSTS ROUTES---------- #


@app.route('/users/<int:user_id>/posts/new')
def create_post(user_id):
    """
    GET ROUTE:
    -Show form to add a post for that user
    """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('new-post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """
    POST ROUTE:
    -Handle add form
    -Add post
    -Redirect to the user detail page
    """
    user = User.query.get_or_404(user_id)
    post_tags = [int(num) for num in request.form.getlist('tags-added')]
    tags = Tag.query.filter(Tag.id.in_(post_tags)).all()

    new_post = Post(
        title=request.form['title'], content=request.form['content'], user_id=user.id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    posts = Post.query.all()

    return redirect(f'/users/{user.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """
    GET ROUTE:
    -Show a post
    -Show buttons to edit and delete the post
    """
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template('post-detail.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """
    GET ROUTE:
    -Show form to edit a post
    -Show button to cancel (redirects to user detail page)
    """
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('edit-post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_edited(post_id):
    """
    POST ROUTE:
    -Handle Editing of a post
    -Redirect back to the post view
    """
    post = Post.query.get_or_404(post_id)
    post_tags = [int(num) for num in request.form.getlist('tags-added')]
    tags = Tag.query.filter(Tag.id.in_(post_tags)).all()

    post.title = request.form['title']
    post.content = request.form['content']
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """
    POST ROUTE:
    -Delete post
    """
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

############################################################
# ----------POSTS ROUTES---------- #


@app.route('/tags')
def list_all_tags():
    """
    GET ROUTE:
    -List all tags
    -Includes links to the tag detail page
    """
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags or None)


@app.route('/tags/<tag_id>')
def show_tag_details(tag_id):
    """
    GET ROUTE:
    -Show detail about a tag
    -Has links to edit form and to delete
    """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-detail.html', tag=tag)


@app.route('/tags/new')
def new_tag_form():
    """
    GET ROUTE:
    -Shows a form to add a new tag
    """
    return render_template('new-tag.html')


@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    """
    POST ROUTE:
    -Process add form
    -Add tag
    -Redirect to tag list
    """
    new_tag = Tag(name=request.form['tag_name'])
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    """
    GET ROUTE:
    -Show edit form for a tag
    """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit-tag.html', tag=tag)


@app.route('/tags/<tag_id>/edit', methods=['POST'])
def execute_edit_tag(tag_id):
    """
    POST ROUTE:
    -Process edit form
    -Edit tag
    -Redirects to the tags list
    """
    edited_tag = Tag.query.get_or_404(tag_id)
    edited_tag.name = request.form['tag_name']

    db.session.add(edited_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """
    POST ROUTE:
    -Delete a tag
    -Redirects to tags list
    """
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
