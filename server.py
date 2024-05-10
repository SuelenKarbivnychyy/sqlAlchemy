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



@app.route("/movies/<movie_id>/rate_movie", methods=["POST"])
def rate_a_movie(movie_id):
    """Rate a movie and save it to the database"""    
    
    user_email = session['user_email']
    score = request.form.get("rating")    

    if not user_email:
        flash("You have to log in")
    elif not score:
        flash("You have to select a rate")    
    else:
        movie = crud.get_movie_by_id(movie_id)
        user = crud.get_user_by_email(user_email)

        rating = crud.create_a_rate(user, movie, int(score))

        db.session.add(rating)
        db.session.commit()    

        flash("Thank you for rating this movie")

    return redirect(f"/movies/{movie_id}")


@app.route("/movies/<movie_id>/rate_movie", methods=["POST"])
def update_rating(movie_id):
    """Update an specific movie"""

    user_id = session("user_id")
    user = crud.get_user_by_id(user_id)
    rating = crud.get_rate_by_user_id(user_id)

    print(f"################## rate from db {rating}")

    new_score = request.form.get("rating")

    if rating:
        flash(f"You've rated this movie as: {rating} points")
        rate = crud.create_a_rate(user.user_id, movie_id, new_score)
        db.session.add(rate)
        db.session.commit()

    return (f"/movies/{movie_id}")


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
    user = crud.get_user_by_email(email)   

    if user:
        flash("Email already have an acount. Try again.")
    else:
        new_user = crud.create_user(email, password)

        db.session.add(new_user)
        db.session.commit()
        flash("Account successfully created, you can now login.")

    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    """Login the user to the page"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    print(f'################### {user}')

    if user == None:
        flash("You need to create an account")
    elif user.password == password:
        flash("Logged in!")
        user_in_session = session['user'] = user.user_id
        print(f'######################## User in session: {user_in_session}')
    else:
        flash("Wrong password. Please try again.")     

    return redirect("/")

    









if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
