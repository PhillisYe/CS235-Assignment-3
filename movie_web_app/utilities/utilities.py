from flask import Blueprint, request, render_template, redirect, url_for, session

import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_rank_and_url():
    rank_urls = dict()
    for rank in range(1000):
        rank_urls[rank] = url_for('movies_bp.movies_by_rank', rank=rank)

    return rank_urls


def get_years_and_urls():
    year_list = services.get_years(repo.repo_instance)
    year_urls = dict()
    for year in year_list:
        year_urls[year] = url_for('movies_bp.movies_by_year', release_year=year)

    return year_urls


def get_genres_and_urls():
    genres_list = services.get_genres_list(repo.repo_instance)
    genre_urls = dict()
    for genre in genres_list:
        genre_urls[genre] = url_for('movies_bp.movies_by_genre', genre=genre)

    return genre_urls


def get_selected_movies(quantity = 10):
    movies = services.get_movies_in_rank(quantity, repo.repo_instance)

    for movie in movies:
        movie['hyperlink'] = url_for('movies_bp.movies_by_rank', rank=movie['rank'])
    return movies

