"""CRUD operations"""

from model import db, User, Movie, Rating, connect_to_db



def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user



def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title,
                overview=overview,
                release_date=release_date,
                poster_path=poster_path)

    return movie


def get_all_movies():
    """Get all movies from the Database and return it."""

    movies = Movie.query.all()

    return movies


def get_movie_by_id(movie_id):
    """Get a movie based on it's Id"""

    movie = Movie.query.get(movie_id)

    return movie



def rating_a_movie(user, movie, score):
    """Create and return a Movie rating."""

    rating = Rating(user=user, movie=movie, score=score)

    return rating












if __name__ == '__main__':
    from server import app
    connect_to_db(app)