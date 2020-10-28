import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from movie_web_app.domain.model import Movie, Director, Actor, Genre, User, Review, WatchList, make_review


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    print(empty_session.query(User).all())
    return keys


def insert_movie(empty_session):
    empty_session.execute(
        'INSERT INTO movies (rank, title, description) VALUES (1, "Guardians of the Galaxy", "A group of '
        'intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the '
        'universe.") '
    )
    row = empty_session.execute('SELECT rank from movies').fetchone()
    return row[0]


def insert_release_year(empty_session):
    empty_session.execute(
        'INSERT INTO release_year (year) VALUES (2013), (2014), (2016)'
    )
    rows = list(empty_session.execute('SELECT year from release_year'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_directors(empty_session):
    empty_session.execute(
        'INSERT INTO directors (name) VALUES ("James Gunn"), ("Ridley Scott")'
    )
    rows = list(empty_session.execute('SELECT id from directors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_actors(empty_session):
    empty_session.execute(
        'INSERT INTO actors (name) VALUES ("Chris Pratt"), ("Vin Diesel"), ("Noomi Rapace")'
    )
    rows = list(empty_session.execute('SELECT id from actors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (name) VALUES ("Action"), ("Adventure"), ("Sci-Fi")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_article_tag_associations(empty_session, article_key, tag_keys):
    stmt = 'INSERT INTO article_tags (article_id, tag_id) VALUES (:article_id, :tag_id)'
    for tag_key in tag_keys:
        empty_session.execute(stmt, {'article_id': article_key, 'tag_id': tag_key})


def insert_reviewed_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, movie_id, review, rating, timestamp) VALUES '
        '(:user_id, :movie_id, "Review 1", 8, :timestamp_1),'
        '(:user_id, :movie_id, "Review 2", 7, :timestamp_2)',
        {'user_id': user_key, 'movie_id': movie_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def make_movie():
    movie = Movie("Moana", 2016)
    return movie


def make_user():
    user = User("Andrew", "111")
    return user


def make_director():
    director = Director("Ron Clements")
    return director


def make_actor():
    actor = Actor("Dwayne Johnson")
    return actor


def make_genre():
    genre = Genre("Animation")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected
