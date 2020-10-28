import pytest

from flask import session

def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please supply another'),
))

def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'YES!MOVIE' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/review?movie=2')

    response = client.post(
        '/review',
        data={'review': 'Who needs quarantine?', 'movie_rank': 2, 'rating': 8}
    )
    assert response.headers['Location'] == 'http://localhost/movies_by_rank?rank=2&view_reviews_for=2'


@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks this movie is a fuckwit?', (b'Your review must not contain profanity')),
        ('Hey', (b'Your review is too short')),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review',
        data={'review': review, 'movie_rank': 2, 'rating': 8}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data



def test_movies_with_year(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_year?release_year=2010')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Inception' in response.data
    assert b'Shutter Island' in response.data


def test_movies_with_review(client,auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/review?movie=40')

    response = client.post(
        '/review',
        data={'review': 'Goooooood!', 'movie_rank': 40, 'rating': 8}
    )
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_rank?rank=40&view_reviews_for=40')
    assert response.status_code == 200

    # Check that all comments for specified article are included on the page.
    assert b'Goooooood!' in response.data
    assert b'8' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_genre?genre=Adventure')
    assert response.status_code == 200

    # Check that all movies tagged with 'Adventure' are included on the page.
    assert b'Prometheus' in response.data
    assert b'Guardians of the Galaxy' in response.data

def test_movies_in_sidebar(client):
    response = client.get('/movies_by_rank?rank=2')
    assert response.status_code == 200

    assert b'Prometheus' in response.data
    assert b'Actors:' in response.data
    assert b'Ridley Scott' in response.data


def test_search_with_actor(client):
    response = client.get('/movies_by_search?q=Chris+Pratt')
    assert response.status_code == 200

    assert b'Search result: Chris Pratt' in response.data
    assert b'Jurassic World' in response.data
    assert b'Chris Pratt' in response.data


def test_search_with_release_year(client):
    response = client.get('/movies_by_search?q=2014')
    assert response.status_code ==200

    assert b'Search result: 2014' in response.data
    assert b'Interstellar' in response.data
    assert b'Guardians of the Galaxy' in response.data

def test_search_with_release_year_second_page(client):
    response = client.get('/movies_by_search?q=2014&cursor=2')
    assert response.status_code == 200

    assert b'Search result: 2014' in response.data
    assert b'John Wick' in response.data
    assert b'Kingsman: The Secret Service' in response.data


def test_search_with_unknown_result(client):
    response = client.get('/movies_by_search?q=Big')
    assert response.status_code == 200

    assert b'Search result: Not Found'
