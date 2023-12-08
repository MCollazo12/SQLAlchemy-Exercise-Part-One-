"""Demo app using SQLAlchemy."""
from flask import Flask, request, redirect, render_template, flash, session


from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'

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
    return render_template("detail.html", user=user, user_id=user_id)


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
