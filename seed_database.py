"""Script to seed database"""

import os
import json
from random import random, randint, choice
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()


with open('data/movies.json') as movie_file:
    movie_data = json.loads(movie_file.read())

movies_in_db = []
for mov in movie_data:
    title = mov['title']
    overview = mov['overview']
    poster_path = mov['poster_path']
    release_date_str = mov['release_date']
    format = "%Y-%m-%d"
    release_date = datetime.strptime(release_date_str, format)


    movie = crud.create_movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    movies_in_db.append(movie)


model.db.session.add_all(movies_in_db)


for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1,5)

        rating = crud.rating_a_movie(user, random_movie, score)
        model.db.session.add(rating)    


model.db.session.commit()


