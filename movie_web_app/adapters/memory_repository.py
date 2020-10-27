import csv
import os

from typing import List, Dict, Set

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from movie_web_app.adapters.repository import AbstractRepository, RepositoryException
from movie_web_app.domain.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.domain.model import Movie, Director, Actor, Genre, User, Review, WatchList, make_review

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__dataset_of_movies: List(Movie) = list()
        self.__dataset_of_release_years = list()
        self.__rank_of_movies: Dict(Movie) = dict()
        self.__movie_details = dict()
        self.__dataset_of_actors: Set(Actor) = set()
        self.__dataset_of_directors: Set(Director) = set()
        self.__dataset_of_genres: Set(Genre) = set()
        self.__movies_with_given_year: Dict(Movie) = dict()
        self.__movies_with_given_director: Dict(Movie) = dict()
        self.__movies_with_given_actor: Dict(Movie) = dict()
        self.__movies_with_given_genre: Dict(Movie) = dict()
        self.__users = list()
        self.__reviews = list()
        self.__user_watch_list: Dict(WatchList) = dict()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.user_name == username), None)

    def get_all_users(self):
        return self.__users

    def add_movie(self, movie: Movie):
        self.__dataset_of_movies.append(movie)

    def get_movie(self, rank: int):
        movie = None

        try:
            movie = self.__rank_of_movies[rank]
        except KeyError:
            pass

        return movie

    def get_movies_by_rank(self, rank_list):
        movies = [self.__rank_of_movies[rank] for rank in rank_list]
        return movies

    def get_number_of_movies(self):
        return len(self.__dataset_of_movies)

    def add_movie_rank(self,rank,movie):
        self.__rank_of_movies[rank] = movie

    def all_movies(self):
        return self.__dataset_of_movies

    #def add_movie_details(self,movie,details):
    #    self.__movie_details[movie] = details

   # def get_movie_details(self, movie:Movie):
    #    return self.__movie_details[movie]
    #def get_movie_director(self, movie: Movie):
    #    return movie.director

    def get_first_movie(self):
        return self.get_movie(1)

    def get_last_movie(self):
        return self.get_movie(1000)

    def add_release_year(self, year):
        if year not in self.__dataset_of_release_years:
            self.__dataset_of_release_years.append(year)

    def get_year_list(self):
        self.__dataset_of_release_years.sort()
        return self.__dataset_of_release_years

    def get_genre_list(self):
        genre_list = list()
        for genre in self.__movies_with_given_genre.keys():
            genre_list.append(genre)
        genre_list.sort()
        return genre_list

    def add_movie_with_release_year(self,movie,year):
        if year not in self.__movies_with_given_year.keys():
            self.__movies_with_given_year[year] = [movie.rank]
        else:
            self.__movies_with_given_year[year].append(movie.rank)

    def get_movie_with_given_year(self, year):
        if year in self.__dataset_of_release_years:
            return self.__movies_with_given_year[year]
        else:
            return list()

    def add_movie_with_actor(self,movie,actors):
        for actor in actors:
            if actor not in self.__movies_with_given_actor:
                self.__movies_with_given_actor[actor] = [movie.rank]
            else:
                self.__movies_with_given_actor[actor].append(movie.rank)

    def get_movie_with_given_actor(self, actor):
        return self.__movies_with_given_actor[actor]

    def add_movie_with_director(self,movie,director):
        if director not in self.__movies_with_given_director:
            self.__movies_with_given_director[director] = [movie.rank]
        else:
            self.__movies_with_given_director[director].append(movie.rank)

    def get_movie_with_given_director(self, director):
        return self.__movies_with_given_director[director]

    def add_movie_with_genre(self,movie,genres):
        for genre in genres:
            if genre not in self.__movies_with_given_genre:
                self.__movies_with_given_genre[genre] = [movie.rank]
            else:
                self.__movies_with_given_genre[genre].append(movie.rank)

    def get_movie_with_given_genre(self, genre):
        return self.__movies_with_given_genre[genre]

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_review(self):
        return self.__reviews

    def have_review(self, review):
        if review in self.__reviews:
            return True

    def add_user_watched_movie(self,user,movie):
        user.watch_movie(movie)

    def get_user_watched_movies(self,user):
        return user.watched_movies

    def add_user_watch_list(self,user,movie):
        if user not in self.__user_watch_list.keys():
            self.__user_watch_list[user] = WatchList()
        self.__user_watch_list[user].add_movie(movie)

    def delete_movie_from_watch_list(self,user,movie):
        if user in self.__user_watch_list.keys():
            self.__user_watch_list[user].remove_movie(movie)

    def get_user_watch_list(self,user):
        if user not in self.__user_watch_list.keys():
            self.__user_watch_list[user] = WatchList()
        return self.__user_watch_list[user]

def read_csv_file(filename):
    with open(filename) as csvfile:
        movie_file_reader = csv.reader(csvfile)

        headers = next(movie_file_reader)

        for row in movie_file_reader:
            row = [item.strip() for item in row]
            yield row

def load_movies(data_path:str, repo: MemoryRepository):
    index = 0
    for row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        rank = int(row[0])
        title = row[1]
        release_year = int(row[6])
        description = row[3]
        runtime = int(row[7])
        movie = Movie(title, release_year)
        movie.rank = rank
        movie.description = description
        movie.runtime_minutes = runtime

        actors = row[5]
        actors_list = actors.split(',')
        for actor in actors_list:
            movie.add_actor(actor)
        director = row[4]
        movie.director = director
        genres = row[2]
        genres_list = genres.split(',')
        for genre in genres_list:
            movie.add_genre(genre)

        repo.add_movie(movie)
        repo.add_movie_rank(rank, movie)
        repo.add_release_year(release_year)

        # add movie with same year into movies_with_given_year
        repo.add_movie_with_release_year(movie,release_year)

        # add movie with same actor into movies_with_given_actor
        repo.add_movie_with_actor(movie,actors)

        # add movie with same director into movies_with_given_director
        repo.add_movie_with_director(movie,director)

        # add movie with same genre into movies_with_given_genre
        repo.add_movie_with_genre(movie,genres_list)

        #repo.add_movie_details(movie,[description, genres_list, runtime, director, actors_list])

        if index > 1000:
            break

        index += 1


def load_users(data_path: str, repo:MemoryRepository):
    users = dict()

    for row in read_csv_file(os.path.join(data_path, 'user.csv')):
        user = User(user_name=row[1],password=generate_password_hash(row[2]))
        repo.add_user(user)
        users[row[0]] = user
    return users


def populate(data_path: str, repo:MemoryRepository):
    load_movies(data_path, repo)
    load_users(data_path, repo)

