from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey123"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
# with app.app_context():
#     db.create_all()


@app.route("/")
def redirect_users():
    return redirect("/users")


@app.route("/users")
def list_users():
    """List users and show add form."""

    users = User.query.all()
    return render_template("/users/users_list.html", users=users)


@app.route("/users/new")
def show_forms():
    return render_template("/users/new_user_form.html")


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
    return render_template("/users/detail.html", user=user)


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
    return render_template("/posts/post_detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_post_edits(post_id):
    """Show form to edit a post or return back to user page"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("/posts/edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_post_edits(post_id):
    """Handle editing of a post. Redirect back to post view."""

    post = Post.query.get_or_404(post_id)
    post.tile = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash("Post edited successfully!", "success")

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the user's post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully!", "success")
    return redirect(f"/users/{post.user_key}")


# -------------------------------- Tag Routes ---------------------------------------
@app.route("/tags")
def list_tags():
    """Lists all tags, with links to the tag detail page."""

    tags = Tag.query.all()
    return render_template("/tags/tags_list.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    """Show detail about a tag with links to edit form and to delete."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tags/tag_detail.html", tag=tag)


@app.route("/tags/new")
def add_tag():
    """Shows a form to add a new tag."""

    posts = Post.query.all()

    return render_template("/tags/new_tag_form.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def add_tag_handler():
    """Handle new tag form submission."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["tag-name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.", "success")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_tag_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("tags/tag_edit.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def handle_tag_edit_form(tag_id):
    """Handle tag edit form submission"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag-name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' was edited.")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Handle the deletion of an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
