from typing import List, Dict, Set
import os

import pytest

from movie_web_app.domain.model import Movie, Director, Actor, Genre, User, Review, make_review
from movie_web_app.adapters import memory_repository
from movie_web_app.adapters.memory_repository import MemoryRepository
from movie_web_app.adapters.repository import RepositoryException

TEST_DATA_PATH = os.path.join(os.sep, 'Users', 'yezi', 'CS235-Assignment-2', 'movie_web_app', 'adapters')

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

def test_repository_can_add_a_user(in_memory_repo):
    user = User("Dave", '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user("dave") is user

def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_movie(in_memory_repo):
    assert in_memory_repo.get_movie(3) == Movie('Split',2016)

def test_repository_can_retrieve_movie_with_rank_list(in_memory_repo):
    rank_list = [1,2,3]
    movies = in_memory_repo.get_movies_by_rank(rank_list)
    assert len(movies) == 3

def test_repository_can_retrieve_first_movie(in_memory_repo):
    assert in_memory_repo.get_first_movie() == Movie("Guardians of the Galaxy", 2014)

def test_repository_can_retrieve_last_movie(in_memory_repo):
    assert in_memory_repo.get_last_movie() == Movie("Nine Lives", 2016)

def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()
    assert number_of_movies == 1000

def test_repository_can_retrieve_movie_with_given_year(in_memory_repo):
    number_of_movies_in_a_year = len(in_memory_repo.get_movie_with_given_year(2016))
    assert number_of_movies_in_a_year == 297

def test_repository_contain_all_the_release_year(in_memory_repo):
    assert in_memory_repo.get_year_list() == [2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]

def test_repository_can_add_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review_text = "This movie was very enjoyable."
    rating = 8
    review = make_review(review_text, user, movie, rating)
    in_memory_repo.add_review(review)
    assert review in in_memory_repo.get_review()

def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "good movie", 8)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

def test_repository_does_not_add_a_review_without_a_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "Trump's onto it!", 8)

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Movie doesn't refer to the Review.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_review()) == 0

#def test_repository_can_retrieve_user_watched_movies(in_memory_repo):
#    user = User("Dave", '123456789')
#    movie = Movie("Moana", 2016)
#    in_memory_repo.add_user(user)
#    in_memory_repo.add_user_watched_movie(user,movie)
#    assert in_memory_repo.get_user_watched_movies(user) == [movie]

#def test_repository_can_retrieve_user_watchlist(in_memory_repo):
#    user = User("Dave", '123456789')
#    movie = Movie("Moana", 2016)
#    in_memory_repo.add_user(user)
#    in_memory_repo.add_user_watch_list(user,movie)
#    assert movie in in_memory_repo.get_user_watch_list(user)

#def test_repository_can_delete_movie_in_user_watchlist(in_memory_repo):
#    user = User("Dave", '123456789')
#    movie = Movie("Moana", 2016)
#    in_memory_repo.add_user(user)
#    in_memory_repo.add_user_watch_list(user,movie)
#    in_memory_repo.delete_movie_from_watch_list(user,movie)
#    assert movie not in in_memory_repo.get_user_watch_list(user)

#def test_repository_does_not_retrieve_a_movie_in_empty_watchlist(in_memory_repo):
#    user = User("Dave", '123456789')
#    movie = Movie("Moana", 2016)
#    in_memory_repo.add_user(user)
 #   assert in_memory_repo.get_user_watch_list(user).size() == 0

def test_repository_return_all_movies(in_memory_repo):
    movies = in_memory_repo.all_movies()
    assert len(movies) == 1000
