from typing import Iterable
import random

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.model import Movie


def get_years(repo: AbstractRepository):
    return repo.get_year_list()


def get_genres_list(repo: AbstractRepository):
    return repo.get_genre_list()


def get_movies_in_rank(quantity, repo: AbstractRepository):
    movie_size = repo.get_number_of_movies()

    if quantity >= movie_size:
        quantity = movie_size - 1

    rank_list = [i for i in range(1, quantity + 1)]
    movies = repo.get_movies_by_rank(rank_list)

    return movies_to_dict(movies)





# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'release_year': movie.release_year,
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
