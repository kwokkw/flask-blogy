"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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


@app.route("/")
def homepage():

    return redirect("/users")
    # return render_template("base.html")


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


@app.route("/users/new", methods=["POST"])
def create_user():

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    url = request.form["image-url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(new_user)
    db.session.commit()

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
    return redirect("/users")


@app.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()

    db.session.commit()
    return redirect("/users")
