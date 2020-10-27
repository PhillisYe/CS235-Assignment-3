from typing import List, Iterable
from datetime import datetime


class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__colleague: List[Actor] = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self) -> str:
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actor):
            return False
        return other.__actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        self.__colleague.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__colleague


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self) -> str:
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other) -> bool:
        # TODO
        if not isinstance(other, Director):
            return False
        return other.__director_full_name == self.__director_full_name

    def __lt__(self, other):
        # TODO
        return self.__director_full_name < other.__director_full_name

    def __hash__(self):
        # TODO
        return hash(self.__director_full_name)


class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self) -> str:
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other) -> bool:
        # TODO
        if not isinstance(other, Genre):
            return False
        return other.__genre_name == self.__genre_name

    def __lt__(self, other):
        # TODO
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        # TODO
        return hash(self.__genre_name)


class User:

    def __init__(self, user_name: str, password: str):
        self.__user_name = user_name.lower().strip()
        self.__password: str = password
        self.__watched_movies: List[Movie] = list()
        self.__reviews: List[Review] = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    def __repr__(self) -> str:
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.__user_name == self.__user_name

    def __lt__(self, other):
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash((self.__user_name, self.__password))

    def watch_movie(self, movie):
        self.__watched_movies.append(movie)
        runtime = movie.runtime_minutes
        self.__time_spent_watching_movies_minutes += runtime

    def add_review(self, review):
        self.__reviews.append(review)


class Review:

    def __init__(self, user: User, movie: 'Movie', review_text: str, rating: int):
        self.__user: User = user
        self.__movie: Movie = movie
        self.__review_text: str = review_text
        if rating >= 1 and rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None
        self.__timestamp = datetime.now()

    @property
    def user(self) -> User:
        return self.__user

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return "{} Rating: {} \nReview: {!r} \n{}".format(self.__movie, self.__rating, self.__review_text,
                                                          self.__timestamp)

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return other.__user == self.__user and \
               other.__movie == self.__movie and \
               other.__review_text == self.__review_text and \
               other.__rating == self.__rating and \
               other.__timestamp == self.__timestamp


class Movie:

    def __init__(self, title: str, release_year: int):
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title
        if release_year < 1900 or type(release_year) is not int:
            self.__release_year = None
        else:
            self.__release_year = release_year
        self.__rank = 0
        self.__description = ""
        self.__director = None
        self.__actors: List[Actor] = list()
        self.__genres: List[Genre] = list()
        self.__runtime_minutes = 0
        self.__rating = 0
        self.__votes = 0
        self.__revenue = 0
        self.__metascores = 0
        self.__reviews: List[Review] = list()

    @property
    def title(self) -> str:
        return self.__title.strip()

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def rank(self) -> int:
        return self.__rank

    @rank.setter
    def rank(self, rank):
        self.__rank = rank

    @property
    def description(self) -> str:
        return self.__description.strip()

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, director):
        director_list = [director]
        if len(director_list) == 1:
            self.__director = director

    @property
    def actors(self):
        return self.__actors

    @property
    def genres(self):
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if runtime_minutes > 0:
            self.__runtime_minutes = runtime_minutes
        else:
            raise ValueError

    @property
    def rating(self) -> float:
        return self.__rating

    @rating.setter
    def rating(self, rating):
        self.__rating = rating

    @property
    def votes(self) -> int:
        return self.__votes

    @votes.setter
    def votes(self, votes):
        self.__votes = votes

    @property
    def revenue(self):
        return self.__revenue

    @revenue.setter
    def revenue(self, revenue):
        self.__revenue = revenue

    @property
    def metascores(self) -> int:
        return self.__metascores

    @metascores.setter
    def metascores(self, metascores):
        self.__metascores = metascores

    @property
    def reviews(self) -> Iterable[Review]:
        return iter(self.__reviews)

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return other.__title == self.__title and other.__release_year == self.__release_year

    def __lt__(self, other):
        return self.__rank < other.__rank

    def __hash__(self):
        return hash((self.__title, self.__release_year))

    def add_actor(self, actor: Actor):
        self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if genre in self.__genres:
            self.__genres.remove(genre)

    def add_review(self, review: Review):
        self.__reviews.append(review)


class WatchList:

    def __init__(self):
        self.__watchlist = list()

    def add_movie(self, movie: Movie):
        if movie not in self.__watchlist:
            self.__watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def select_movie_to_watch(self, index):
        if index >= len(self.__watchlist) or index < 0:
            return None
        else:
            return self.__watchlist[index]

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        if self.__watchlist == []:
            return None
        else:
            return self.__watchlist[0]

    def __repr__(self):
        return "{}".format(self.__watchlist)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.__watchlist):
            result = self.__watchlist[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration


def make_review(review_text: str, user: User, movie: Movie, rating: int):
    review = Review(user, movie, review_text, rating)
    user.add_review(review)
    movie.add_review(review)

    return review

