from dataclasses import dataclass


@dataclass
class MongoMoviesUpdate:
    imdb_code: str
