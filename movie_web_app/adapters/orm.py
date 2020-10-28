from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie_web_app.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.rank')),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('rank', Integer, primary_key=True), #autoincrement=True),
    Column('release_year', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    #Column('director', String(255), nullable=False),
    #Column('actor', String(255), nullable=False),
    #Column('genre', String(255), nullable=False)
)

release_years = Table(
    'release_year', metadata,
    Column('year', Integer, primary_key=True)
)

movie_years = Table(
    'movie_year', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.rank')),
    Column('year', ForeignKey('release_year.year'))
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movie_directors = Table(
    'movie_director', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.rank')),
    Column('director_id', ForeignKey('directors.id'))
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.rank')),
    Column('actor_id', ForeignKey('actors.id'))
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.rank')),
    Column('genre_id', ForeignKey('genres.id'))
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '__user_name': users.c.username,
        '__password': users.c.password,
        '__reviews': relationship(model.Review, backref='__user')
    })
    mapper(model.Review, reviews, properties={
        '__review_text': reviews.c.review,
        '__rating': reviews.c.rating,
        '__timestamp': reviews.c.timestamp
    })

