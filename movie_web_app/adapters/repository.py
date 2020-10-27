import abc
from typing import List

from movie_web_app.domain.model import Movie, Actor, Genre, Director, User, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_users(self):
        raise NotImplementedError


    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, rank):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_rank(self, rank_list):
        """Returns Movie with rank from the repository.

        If there is no Movie with the given rank, this method returns None."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_rank(self, rank, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def all_movies(self):
        raise NotImplementedError

    #@abc.abstractmethod
    ##def add_movie_details(self, movie, details):
        raise NotImplementedError

    #@abc.abstractmethod
    #def get_movie_details(self, movie: Movie):
    #    """Return the details of Movie from the repository."""
    #    raise NotImplementedError

    #@abc.abstractmethod
    #def get_movie_director(self, movie):
    #    raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_release_year(self, year):
        raise NotImplementedError

    @abc.abstractmethod
    def get_year_list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre_list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_with_given_year(self, year):
        """Return the Movies with a given year from the repository.

        If there is no Movie with the given year, this method returns None."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_with_given_actor(self, actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_with_given_director(self, director):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_with_given_genre(self, genre):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """Adds a Review to the repository."""
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Review not correctly attached to a Movie')

    @abc.abstractmethod
    def get_review(self):
        """Return the review of a Movie stored in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_watched_movies(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user_watch_list(self, user, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_movie_from_watch_list(self, user, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_watch_list(self, user):
        raise NotImplementedError
