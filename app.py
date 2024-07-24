"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:Kwok17273185@localhost:5432/blogly"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "secret_key"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# USERS ROUTES ##################################################################


@app.route("/")
def homepage():

    created_at = Post.created_at.desc()
    posts = Post.query.order_by(created_at).all()
    return render_template("base.html", posts=posts)


@app.route("/users")
def show_all_users():

    # `User.query`: Accesses the query object for the User table.
    # `User.last_name` and `User.first_name`: Refer to the columns in the `User` table to specify the sort order.
    # `order_by(...).all()`: Constructs and executes the query, returning a list of User instances.
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def show_form():
    return redirect("/new")


# Add new user
@app.route("/users/new", methods=["POST"])
def create_user():

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    url = request.form["image-url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(new_user)
    db.session.commit()

    flash(f"User {new_user.full_name} has been created.")
    return redirect("/users")


@app.route("/new")
def new_user():
    return render_template("/new.html")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/user/<int:user_id>/edit")
def show_edit_page(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("/edit.html", user=user)


@app.route("/user/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    # Update user
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["imgae-url"]
    db.session.commit()

    flash(f"{user.full_name} info has been updated.")
    return redirect("/users")


@app.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.full_name} deleted.")
    return redirect("/users")


# POSTS ROUTES ##################################################################


# Show form to add a post for that user.
@app.route("/user/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("/add-post.html", user=user)


# Handle add form
@app.route("/user/<int:user_id>/post/new", methods=["POST"])
def handle_add_form(user_id):
    user = User.query.get_or_404(user_id)

    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    flash(f"New post '{title}' has been added.")
    return redirect(f"/users/{user.id}")


# Show a post. Show buttons to edit and delete the post.
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("show-post.html", post=post)


# Show form to edit a post, and to cancel (back to user page).
@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.html", post=post)


# Handle editing of a post. Redirect back to the post view.
@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_editing_post(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content
    db.session.commit()

    flash(f"Post '{title}' has been updated.")
    return redirect(f"/posts/{post.id}")


# **POST */posts/[post-id]/delete :*** Delete the post.
@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' has been deleted.")
    return redirect(f"/users/{post.user_id}")
