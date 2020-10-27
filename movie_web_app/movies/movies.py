from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length, ValidationError

import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.utilities as utilities
import movie_web_app.movies.services as services

from movie_web_app.authentication.authentication import login_required

from urllib.request import urlopen
import urllib.parse
import ast

# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies_by_rank', methods=['GET'])
def movies_by_rank():
    # Read query parameters.
    target_rank = request.args.get('rank')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_rank is None:
        # No rank query parameter, so return movies from rank 1 of the series.
        target_rank = 1
    else:
        # Convert target_rank from string to int.
        target_rank = int(target_rank)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) for the target rank. This call also returns the previous and next rank for movies immediately
    # before and after the target rank.
    movie = services.get_movie(target_rank, repo.repo_instance)
    movie_image = {}
    title = movie["title"]
    args = {"t": title}
    link = "http://www.omdbapi.com/?{}&apikey=4421208f".format(urllib.parse.urlencode(args))
    response = urlopen(link)
    content = response.read()
    content_dict = content.decode("UTF-8")
    detail = ast.literal_eval(content_dict)
    image = detail["Poster"]
    movie_image[movie["title"]] = image

    previous_rank = target_rank - 1
    next_rank = target_rank + 1

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movie) > 0:
        # There's one movie for the target rank.
        if previous_rank is not None:
            # There are movie on a previous rank, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_rank', rank=previous_rank)
            first_movie_url = url_for('movies_bp.movies_by_rank', rank=first_movie['rank'])

        # There is a movie on a subsequent rank, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_rank is not None:
            next_movie_url = url_for('movies_bp.movies_by_rank', rank=next_rank)
            last_movie_url = url_for('movies_bp.movies_by_rank', rank=last_movie['rank'])

        # Construct urls for viewing movie reviews and adding reviews.
        movie['view_review_url'] = url_for('movies_bp.movies_by_rank', rank=target_rank, view_reviews_for=movie['rank'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title='Movie',
            movies_title='Rank' + str(target_rank),
            movies=[movie],
            image=movie_image,
            selected_movies=utilities.get_selected_movies(10),
            rank_urls=utilities.get_rank_and_url(),
            year_urls=utilities.get_years_and_urls(),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews,
        )

    # No articles to show, so return the homepage.
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/movies_by_year', methods=['GET'])
def movies_by_year():
    movies_per_page = 2

    # Read query parameters.
    year = request.values.get('release_year')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    year = int(year)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie to show reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ranks for movies that are released in that year.
    movie_ranks = services.get_movie_ranks_for_year(year, repo.repo_instance)
    #movie_ranks = services.get_movies_by_year(year, repo.repo_instance)
    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)
    movies_image = {}
    for movie in movies:
        title = movie["title"]
        args = {"t": title}
        link = "http://www.omdbapi.com/?{}&apikey=4421208f".format(urllib.parse.urlencode(args))
        response = urlopen(link)
        content = response.read()
        content_dict = content.decode("UTF-8")
        detail = ast.literal_eval(content_dict)
        image = detail["Poster"]
        movies_image[movie["title"]] = image

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_year', release_year=year, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_year', release_year=year)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_year', release_year=year, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_year', release_year=year, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_year', release_year=year, cursor=cursor,
                                           view_reviews_for=movie['rank'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        #title='Movies',
        movies_title='Movies released in ' + str(year),
        #release_year=year,
        movies=movies,
        image=movies_image,
        selected_movies=utilities.get_selected_movies(10),#len(movies) * 2),
        year_urls=utilities.get_years_and_urls(),
        genre_urls=utilities.get_genres_and_urls(),
        rank_urls=utilities.get_rank_and_url(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
    )


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 2

    # Read query parameters.
    genre = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ranks for movies that are tagged with genre.
    movie_ranks = services.get_movie_ranks_for_genre(genre, repo.repo_instance)

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)

    movies_image = {}
    for movie in movies:
        title = movie["title"]
        args = {"t": title}
        link = "http://www.omdbapi.com/?{}&apikey=4421208f".format(urllib.parse.urlencode(args))
        response = urlopen(link)
        content = response.read()
        content_dict = content.decode("UTF-8")
        detail = ast.literal_eval(content_dict)
        image = detail["Poster"]
        movies_image[movie["title"]] = image

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre, cursor=cursor,
                                           view_reviews_for=movie['rank'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        #title='Movies',
        movies_title='Movies in ' + genre,
        movies=movies,
        image=movies_image,
        selected_movies=utilities.get_selected_movies(10),#len(movies) * 2),
        year_urls=utilities.get_years_and_urls(),
        genre_urls=utilities.get_genres_and_urls(),
        rank_urls=utilities.get_rank_and_url(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
    )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie rank, representing the reviewed movie, from the form.
        movie_rank = int(form.movie_rank.data)

        # Use the service layer to store the new review.
        services.add_review(movie_rank, form.review.data, form.rating.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_rank, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movies_bp.movies_by_rank', rank=movie['rank'], view_reviews_for=movie_rank))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie rank, representing the movie to review, from a query parameter of the GET request.
        movie_rank = int(request.args.get('movie'))

        # Store the movie rank in the form.
        form.movie_rank.data = movie_rank
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie rank of the movie being reviewed from the form.
        movie_rank = int(form.movie_rank.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_rank, repo.repo_instance)
    return render_template(
        'movies/review_on_movie.html',
        title='Review of movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_on_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        year_urls=utilities.get_years_and_urls(),
        rank_urls=utilities.get_rank_and_url(),
    )


@movies_blueprint.route('/movies_by_search', methods=['GET', 'POST'])
def movies_by_search():
    movies_per_page = 2

    q = request.args.get('q')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    all_movies = services.get_all_movies(repo.repo_instance)
    movie_ranks = []
    if q:
        for movie in all_movies:
            try:
                q = int(q)
                if q in movie.values():
                    if movie['rank'] not in movie_ranks:
                        movie_ranks.append(movie['rank'])
            except:
                pass
            if q in movie.values() or q in movie['actors'] or q in movie['genres']:
                if movie['rank'] not in movie_ranks:
                    movie_ranks.append(movie['rank'])

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)


    movies_image = {}
    for movie in movies:
        title = movie["title"]
        args = {"t": title}
        link = "http://www.omdbapi.com/?{}&apikey=4421208f".format(urllib.parse.urlencode(args))
        response = urlopen(link)
        content = response.read()
        content_dict = content.decode("UTF-8")
        detail = ast.literal_eval(content_dict)
        image = detail["Poster"]
        movies_image[movie["title"]] = image

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_search', q=q, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_search', q=q)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_search', q=q, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_search', q=q, cursor=last_cursor)

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movies:
            movie['view_review_url'] = url_for('movies_bp.movies_by_search', q=q, cursor=cursor,
                                                   view_reviews_for=movie['rank'])
            movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['rank'])

    if movie_ranks == []:
        return render_template(
            'movies/movies.html',
            movies_title='Search result: Not Found',
            #movies=movies,
            selected_movies=utilities.get_selected_movies(10),
            year_urls=utilities.get_years_and_urls(),
            genre_urls=utilities.get_genres_and_urls(),
            rank_urls=utilities.get_rank_and_url(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews,
        )

    return render_template(
        'movies/movies.html',
        movies_title='Search result: ' + str(q),
        movies=movies,
        image=movies_image,
        selected_movies=utilities.get_selected_movies(10),
        year_urls=utilities.get_years_and_urls(),
        genre_urls=utilities.get_genres_and_urls(),
        rank_urls=utilities.get_rank_and_url(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = SelectField('Rating', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], coerce=int)
    movie_rank = HiddenField("Movie rank")
    submit = SubmitField('Submit')
