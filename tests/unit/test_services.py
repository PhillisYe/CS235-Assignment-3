from datetime import date

import pytest

from movie_web_app.authentication.services import AuthenticationException
from movie_web_app.domain.model import Movie
from movie_web_app.movies import services as movies_services
from movie_web_app.authentication import services as auth_services
from movie_web_app.movies.services import NonExistentMovieException

def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_rank = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the review.
    movies_services.add_review(movie_rank, review_text, 8, username, in_memory_repo)

    # Retrieve the reviews for the movie from the repository.
    reviews_as_dict = movies_services.get_reviews_for_movie(movie_rank, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_rank = 1001
    review_text = "Movie - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_rank, review_text, 8, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_rank = 3
    review_text = 'Good!'
    username = 'gmichael'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(movie_rank, review_text, 8, username, in_memory_repo)


def test_can_get_review(in_memory_repo):
    movie_rank = 2

    movie_as_dict = movies_services.get_movie(movie_rank, in_memory_repo)

    assert movie_as_dict['rank'] == movie_rank
    assert movie_as_dict['title'] == 'Prometheus'
    assert movie_as_dict['release_year'] == 2012
    assert movie_as_dict['description'] == "Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone."
    assert movie_as_dict['director'] == 'Ridley Scott'
    assert movie_as_dict['runtime'] == 124
    assert len(movie_as_dict['reviews']) == 0

    #tag_names = [dictionary['name'] for dictionary in article_as_dict['tags']]
    #assert 'World' in tag_names
    #assert 'Health' in tag_names
    #assert 'Politics' in tag_names


def test_cannot_get_movie_with_non_existent_rank(in_memory_repo):
    rank = 1005

    # Call the service layer to attempt to retrieve the Movie.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(rank, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movies_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['rank'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movies_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['rank'] == 1000


def test_get_movies_by_year(in_memory_repo):
    target_year = 2016

    movies_as_dict = movies_services.get_movies_by_year(target_year, in_memory_repo)

    # Check that there are 3 movies in year 2016.
    assert len(movies_as_dict) == 297

    # Check that the movie ranks for the the movies returned are 3, 4 and 5.
    movie_ranks = [movie['rank'] for movie in movies_as_dict]
    assert set([3, 4, 5]).issubset(movie_ranks)


def test_get_movies_by_year_with_non_existent_year(in_memory_repo):
    target_date = 2020

    movies_as_dict = movies_services.get_movies_by_year(target_date, in_memory_repo)

    # Check that there are no articles in year 2020.
    assert len(movies_as_dict) == 0


def test_get_movies_by_rank(in_memory_repo):
    target_movie_ranks = [5, 6]
    movies_as_dict = movies_services.get_movies_by_rank(target_movie_ranks, in_memory_repo)

    # Check that 2 articles were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the article ids returned were 5 and 6.
    movie_titles = [movie['title'] for movie in movies_as_dict]

    assert set(['Suicide Squad', 'The Great Wall']).issubset(movie_titles)


def test_get_reviews_for_movie(in_memory_repo):
    movies_services.add_review(1,"Good",8,'fmercury',in_memory_repo)
    reviews_as_dict = movies_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 1 review were returned for article with id 1.
    assert len(reviews_as_dict) == 1

    # Check that the review relate to the movie whose rank is 1.
    movie_ranks = [review['movie_rank'] for review in reviews_as_dict]
    movie_ranks = set(movie_ranks)
    assert 1 in movie_ranks and len(movie_ranks) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movies_services.get_reviews_for_movie(1005, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(reviews_as_dict) == 0

