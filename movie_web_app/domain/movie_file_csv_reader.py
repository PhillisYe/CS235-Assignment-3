import csv
from typing import List, Dict, Set
from movie_web_app.domain.model import Movie, Actor, Genre, Director

class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies: List(Movie) = list()
        self.__dataset_of_actors: Set(Actor) = set()
        self.__dataset_of_directors: Set(Director) = set()
        self.__dataset_of_genres: Set(Genre) = set()
        self.__rank_of_movies: Dict(Movie) = dict()
        self.__movies_with_given_year: Dict(Movie) = dict()
        self.__movies_with_given_director: Dict(Movie) = dict()
        self.__movies_with_given_actor: Dict(Movie) = dict()
        self.__movies_with_given_genre: Dict(Movie) = dict()

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    @property
    def rank_of_movies(self):
        return self.__rank_of_movies

    @rank_of_movies.setter
    def rank_of_movies(self, rank):
        return self.__rank_of_movies[rank]

    @property
    def movies_with_given_year(self):
        return self.__movies_with_given_year

    @movies_with_given_year.setter
    def movies_with_given_year(self, year):
        return self.__movies_with_given_year[year]

    @property
    def movies_with_given_actor(self):
        return self.__movies_with_given_actor

    @movies_with_given_actor.setter
    def movies_with_given_actor(self, actor):
        return self.__movies_with_given_actor[actor]

    @property
    def movies_with_given_director(self):
        return self.__movies_with_given_director

    @movies_with_given_director.setter
    def movies_with_given_director(self, director):
        return self.__movies_with_given_director[director]

    @property
    def movies_with_given_genre(self):
        return self.__movies_with_given_genre

    @movies_with_given_genre.setter
    def movies_with_given_genre(self, genre):
        return self.__movies_with_given_genre[genre]

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                rank = row['Rank']
                title = row['Title']
                release_year = int(row['Year'])
                self.__dataset_of_movies.append(Movie(title, release_year))
                self.__rank_of_movies[rank] = Movie(title, release_year)

                # add movie with same year into movies_with_given_year
                if release_year not in self.__movies_with_given_year.keys():
                    self.__movies_with_given_year[release_year] = [Movie(title, release_year)]
                else:
                    movie = Movie(title, release_year)
                    self.__movies_with_given_year[release_year].append(movie)

                actors = row['Actors']
                actors_list = actors.split(',')
                for actor in actors_list:
                    if actor not in self.__dataset_of_actors:
                        self.__dataset_of_actors.add(Actor(actor))

                # add movie with same actor into movies_with_given_actor
                for actor in actors_list:
                    if actor not in self.__movies_with_given_actor:
                        self.__movies_with_given_actor[actor] = [Movie(title, release_year)]
                    else:
                        self.__movies_with_given_actor[actor].append(Movie(title, release_year))

                director = row['Director']
                if director not in self.__dataset_of_directors:
                    self.__dataset_of_directors.add(Director(director))

                #add movie with same director into movies_with_given_director
                if director not in self.__movies_with_given_director:
                    self.__movies_with_given_director[director] = [Movie(title, release_year)]
                else:
                    self.__movies_with_given_director[director].append(Movie(title, release_year))

                genres = row['Genre']
                genres_list = genres.split(',')
                for genre in genres_list:
                    if genre not in self.__dataset_of_genres:
                        self.__dataset_of_genres.add(Genre(genre))

                #add movie with same genre into movies_with_given_genre
                for genre in genres_list:
                    if genre not in self.__movies_with_given_genre:
                        self.__movies_with_given_genre[genre] = [Movie(title, release_year)]
                    else:
                        self.__movies_with_given_genre[genre].append(Movie(title, release_year))

                if index > 1000:
                    break

                index += 1
