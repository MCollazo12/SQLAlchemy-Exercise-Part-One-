"""Demo app using SQLAlchemy."""
from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey123"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


@app.route("/")
def redirect_users():
    return redirect("/users")


@app.route("/users")
def list_users():
    """List users and show add form."""

    users = User.query.all()
    return render_template("users_list.html", users=users)


@app.route("/users/new")
def show_forms():
    return render_template("new_user_form.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Add user and redirect back to list of users."""

    default_img = "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    # Validate input fields
    if not first_name or not last_name:
        flash("First name and last name are required.", "error")
        return redirect("/users/new")

    # Add default image if image URL is not provided
    image_url = image_url if image_url else default_img

    # Add user to database
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash("User added successfully!", "success")
    return redirect("/users")


# Route to show information about a specific user
@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)


# Route to show the edit page for a user
@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show edit page for a user"""

    # Find user using get_user class method
    user = User.get_user(user_id)
    if user:
        return render_template(
            "edit_user_form.html",
            user_id=user.id,
            user_first_name=user.first_name,
            user_last_name=user.last_name,
            user_image_url=user.image_url,
        )
    else:
        return "User not found", 404


# Route to process the edit form for a user
@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_user_form(user_id):
    user = User.get_user(user_id)
    if user:
        # Update user information (replace this with your logic)
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.image_url = request.form["image_url"]

        db.session.commit()

        return redirect(f"/users/{user_id}")
    else:
        return "User not found", 404


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    user = User.get_user(user_id)
    if user:
        # Delete user from the database
        db.session.delete(user)
        db.session.commit()

        return redirect("/users")
    else:
        return "User not found", 404


@app.route("/users/<int:user_id>/posts/new")
def new_user_post(user_id):
    """Show form to add a post for that user"""

    user = User.query.get_or_404(user_id)
    return render_template("new_post_form.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def process_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""

    user = User.query.get_or_404(user_id)

    title = request.form["title"]
    content = request.form["content"]

    # Validate input fields
    if not title or not content:
        flash("Title and content are required", "error")
        return redirect(f"users/{user_id}/posts/new")

    # Add post to the user's posts
    post = Post(
        title=title, content=content, created_at=datetime.utcnow(), user_key=user_id
    )
    db.session.add(post)
    db.session.commit()

    flash("Post added successfuly!", "success")
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a single post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_post_edits(post_id):
    """Show form to edit a post or return back to user page"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_post_edits(post_id):
    """Handle editing of a post. Redirect back to post view."""

    post = Post.query.get_or_404(post_id)

    post.tile = request.form["title"]
    post.content = request.form["content"]

    db.session.commit()

    flash("Post edited successfully!", "success")
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """Delete the user's post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully!", "success")
    return redirect(f"/users/{post.user_key}")
