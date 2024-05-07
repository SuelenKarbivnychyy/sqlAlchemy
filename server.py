"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.indefined = StrictUndefined


@app.route("/")
def homepage():
    """View Homepage."""

    return render_template("homepage.html")


@app.route("/movies")
def all_movies():
    """Display all movies"""

    movies = crud.get_all_movies()

    return render_template("all_movies.html", movies=movies)


@app.route("/movies/<movie_id>")
def display_movie_details(movie_id):
    """Display details on a particular movie."""    

    movie = crud.get_movie_by_id(movie_id)   

    return render_template("movie_details.html", movie=movie)


@app.route("/all_users")
def display_all_users():
    """Display all users from database."""

    users = crud.get_all_users()

    return render_template("all_users.html", users=users)


@app.route("/all_users/<user_id>")
def display_user_profile(user_id):
    """Display user's profile."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_profile.html", user=user)


@app.route("/users", methods=["POST"])
def register_user():
    """Check if user is on database, if it's not, add it to the database."""

    email = request.form.get("email")
    password = request.form.get("password")

    is_user_in_db = crud.get_user_by_email(email)   

    if is_user_in_db:
        flash("Email already have an acount. Try again.")
    else:
        new_user = crud.create_user(email, password)

        db.session.add(new_user)
        db.session.commit()
        flash("Account successfully created, you can now login.")

    return redirect("/")   









if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
