from typing import List, Iterable

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.model import Movie, Director, Actor, Genre, User, Review, WatchList, make_review


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def get_user(repo: AbstractRepository):
    return repo.get_all_users()

def add_review(movie_rank: int, review_text: str, rating: int, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(review_text, user, movie, rating)

    # Update the repository.
    repo.add_review(review)


def get_movie(rank: int, repo: AbstractRepository):
    movie = repo.get_movie(rank)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()

    return movie_to_dict(movie)


def get_movies_by_year(year, repo: AbstractRepository):
    # Returns movies for the target year (empty if no matches), the date of the previous article (might be null), the date of the next article (might be null)
    movies = repo.get_movie_with_given_year(year)

    movies_dto = list()
    #prev_date = next_date = None

    if len(movies) > 0:
        #prev_date = repo.get_date_of_previous_article(articles[0])
        #next_date = repo.get_date_of_next_article(articles[0])

        # Convert Articles to dictionary form.
        movies_name = list()
        for movie_rank in movies:
            movies_name.append(repo.get_movie(movie_rank))
        movies_dto = movies_to_dict(movies_name)

    return movies_dto


def get_movie_ranks_for_year(year, repo: AbstractRepository):
    movie_ranks = repo.get_movie_with_given_year(year)

    return movie_ranks


def get_movie_ranks_for_genre(genre, repo: AbstractRepository):
    movie_ranks = repo.get_movie_with_given_genre(genre)
    return movie_ranks


def get_movies_by_rank(rank_list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_all_movies(repo: AbstractRepository):
    movies = repo.all_movies()

    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_rank, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'genres': movie.genres,
        'runtime': movie.runtime_minutes,
        'reviews': reviews_to_dict(movie.reviews),
        #'years': years_to_dict(movie.release_year)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user,
        'movie_rank': review.movie.rank,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp,
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


#def year_to_dict(movie:Movie):
 #   year_dict = {
 #       'year': movie.release_year,
 #       'movies_with_year': [movie.rank for movie in tag.tagged_articles]
 #   }
 #   return year_dict


#def years_to_dict(years):
 #   return [year_to_dict(tag) for tag in tags]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.release_year)
    # Note there's no comments or tags.
    return movie