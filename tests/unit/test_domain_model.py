from movie_web_app.domain.model import Movie, Actor, Genre, Director, User, Review, WatchList, make_review
import pytest

@pytest.fixture()
def movie():
    return Movie("Moana", 2016)

@pytest.fixture()
def actor():
    return Actor("Angelina Jolie")

@pytest.fixture()
def director():
    return Director("Ron Clements")

@pytest.fixture()
def user():
    return User('Martin','pw12345')

@pytest.fixture()
def watchlist():
    return WatchList()

def test_actor_construction(actor):
    actor.add_actor_colleague("Bob")
    assert actor.check_if_this_actor_worked_with("Bob")


def test_movie_construction(movie):
    movie.runtime_minutes = 107
    assert "Movie runtime: {} minutes".format(movie.runtime_minutes) == "Movie runtime: 107 minutes"

def test_user_construction(user):
    assert user.user_name == 'martin'
    assert user.password == 'pw12345'
    assert repr(user) == '<User martin>'

    for review in user.reviews:
        assert False

    movie = Movie("Moana", 2016)
    movie.runtime_minutes = 107
    user.watch_movie(movie)
    assert user.time_spent_watching_movies_minutes == 107

def test_write_reviews(movie,user):
    review_text = "This movie was very enjoyable."
    rating = 8
    review = make_review(review_text, user, movie,rating)

    assert review in user.reviews
    assert review.user is user
    assert review in movie.reviews
    assert review.movie is movie

def test_watchlist_construction(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.size() == 3

    watchlist.remove_movie(Movie("Moana", 2016))
    assert watchlist.size() == 2
    assert repr(watchlist.first_movie_in_watchlist()) == '<Movie Ice Age, 2002>'

    assert repr(watchlist.select_movie_to_watch(1)) == '<Movie Guardians of the Galaxy, 2012>'
    assert watchlist.select_movie_to_watch(3) == None

