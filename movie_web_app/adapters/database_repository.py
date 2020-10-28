import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie_web_app.domain.model import Movie, Director, Actor, Genre, User, Review, WatchList
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.movie_file_csv_reader import MovieFileCSVReader

tags = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(__user_name=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_all_users(self):
        return self._session_cm.session.query(User).all()

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, rank: int):
        movie = None

        try:
            movie = self._session_cm.session.query(Movie).filter(_Movie__rank=rank).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_rank(self, rank) -> List[Movie]:
        if rank is None:
            movies = self._session_cm.session.query(Movie).all()
            return movies
        else:
            # Return movies matching rank_list; return an empty list if there are no matches.
            movies = self._session_cm.session.query(Movie).filter(_Movie__rank == rank).all()
            return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    #def add_movie_rank(self, rank, movie):
    #    self.__rank_of_movies[rank] = movie

    def all_movies(self):
        movies = self._session_cm.session.query(Movie).all()
        return movies

    def get_first_movie(self):
        movie = self._session_cm.session.query(Movie).first()
        return movie

    def get_last_movie(self):
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie.__rank)).first()
        return movie

    #def add_release_year(self, year):
    #    if year not in self.__dataset_of_release_years:
    #        self.__dataset_of_release_years.append(year)

    #def get_year_list(self):
    #    year = self._session_cm.session.query(Movie.__release_year).order_by(asc(Movie.__release_year)).all()
    #    return year

    #def get_genre_list(self):
    #    genre_list = list()
    #    for genre in self.__movies_with_given_genre.keys():
    ##        genre_list.append(genre)
    #    genre_list.sort()
    #    return genre_list

    #def add_movie_with_release_year(self, movie, year):
    #    if year not in self.__movies_with_given_year.keys():
    #        self.__movies_with_given_year[year] = [movie.rank]
    #    else:
    #        self.__movies_with_given_year[year].append(movie.rank)

    def get_movie_with_given_year(self, year):
        movie_ranks = []

        # Use native SQL to retrieve movie ranks, since there is no mapped class for the movie_years table.
        row = self._session_cm.session.execute('SELECT rank FROM movies WHERE release_year = :year', {'year': year}).fetchone()

        if row is None:
            # No movie with given year - create an empty list.
            movie_ranks = list()
        else:
            movie_ranks = row

        return movie_ranks

    #def add_movie_with_actor(self, movie, actors):
    #    with self._session_cm as scm:
    #        scm.session.add()
    #    for actor in actors:
    #        if actor not in self.__movies_with_given_actor:
    #            self.__movies_with_given_actor[actor] = [movie.rank]
    #        else:
    #            self.__movies_with_given_actor[actor].append(movie.rank)

    def get_movie_with_given_actor(self, actor):
        movie_ranks = []

        row = self._session_cm.session.execute('SELECT id FROM actors WHERE name = :actor', {'actor': actor}).fetchone()

        if row is None:
            # No actor with give actor name - create an empty list.
            movie_ranks = list()
        else:
            actor_id = row[0]

            # retrieve movie ranks of movies associated with the actor.
            movie_ranks = self._session_cm.session.execute('SELECT movie_id FROM movie_actors WHERE actor_id = '
                                                           ':actor_id ORDER BY movie_id ASC', {'actor_id': actor_id}
                                                           ).fetchall()
            movie_ranks = [id[0] for id in movie_ranks]
        return movie_ranks

    #def add_movie_with_director(self, movie, director):
    #    if director not in self.__movies_with_given_director:
    #        self.__movies_with_given_director[director] = [movie.rank]
    #    else:
    #        self.__movies_with_given_director[director].append(movie.rank)

    def get_movie_with_given_director(self, director):
        movie_ranks = []

        row = self._session_cm.session.execute('SELECT id FROM directors WHERE name = :director', {'director': director}
                                               ).fetchone()

        if row is None:
            # No actor with give actor name - create an empty list.
            movie_ranks = list()
        else:
            director_id = row[0]

            # retrieve movie ranks of movies associated with the director.
            movie_ranks = self._session_cm.session.execute('SELECT movie_id FROM movie_directors WHERE director_id = '
                                                           ':director_id ORDER BY movie_id ASC',
                                                           {'director_id': director_id}).fetchall()
            movie_ranks = [id[0] for id in movie_ranks]
        return movie_ranks

    #def add_movie_with_genre(self, movie, genres):
    #    for genre in genres:
    #        if genre not in self.__movies_with_given_genre:
    #            self.__movies_with_given_genre[genre] = [movie.rank]
    #        else:
    #            self.__movies_with_given_genre[genre].append(movie.rank)

    def get_movie_with_given_genre(self, genre):
        movie_ranks = []

        row = self._session_cm.session.execute('SELECT id FROM genres WHERE name = :genre', {'genre': genre}).fetchone()

        if row is None:
            # No genre with give genre name - create an empty list.
            movie_ranks = list()
        else:
            genre_id = row[0]

            # retrieve movie ranks of movies associated with the genre.
            movie_ranks = self._session_cm.session.execute('SELECT movie_id FROM movie_genres WHERE genre_id = '
                                                           ':genre_id ORDER BY movie_id ASC', {'genre_id': genre_id}
                                                           ).fetchall()
            movie_ranks = [id[0] for id in movie_ranks]
        return movie_ranks

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_review(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def have_review(self, review):
        result = self._session_cm.session.query(Review).filter(Review.__review_text.in_(review)).all()
        if len(review) > 0:
            return True

    #def add_user_watched_movie(self, user, movie):
    #    user.watch_movie(movie)

    #def get_user_watched_movies(self, user):
     #   return user.watched_movies

    #def add_user_watch_list(self, user, movie):
    #    if user not in self.__user_watch_list.keys():
    #        self.__user_watch_list[user] = WatchList()
    #    self.__user_watch_list[user].add_movie(movie)

    #def delete_movie_from_watch_list(self, user, movie):
    #    if user in self.__user_watch_list.keys():
    #        self.__user_watch_list[user].remove_movie(movie)

    #def get_user_watch_list(self, user):
    #    if user not in self.__user_watch_list.keys():
    #        self.__user_watch_list[user] = WatchList()
    #    return self.__user_watch_list[user]

def populate(session_factory, data_path: str, data_filename):

    filename = os.path.join(data_path, data_filename)
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    session = session_factory()

    # This takes all movies from the csv file (represented as domain model objects) and adds them to be
    # database. If the uniqueness of directors, actors, genres is correctly handled, and the relationships
    # are correctly set up in the ORM mapper, then all associations will be dealt with as well!
    for director in movie_file_reader.dataset_of_directors:
        session.add(director)

    for actor in movie_file_reader.dataset_of_actors:
        session.add(actor)

    for genre in movie_file_reader.dataset_of_genres:
        session.add(genre)


    session.commit()

