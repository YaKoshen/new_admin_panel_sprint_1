import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Filmwork:
    description: str
    creation_date: datetime
    rating: float
    type: str
    file_path: str
    title: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default=datetime.now())
    modified: datetime = field(default=datetime.now())


@dataclass(frozen=True)
class Genre:
    description: str
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default=datetime.now())
    modified: datetime = field(default=datetime.now())


@dataclass(frozen=True)
class GenreFilmwork:
    filmwork_id: uuid.UUID
    genre_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default=datetime.now())


@dataclass(frozen=True)
class Person:
    full_name: str
    gender: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default=datetime.now())
    modified: datetime = field(default=datetime.now())


@dataclass(frozen=True)
class PersonFilmwork:
    role: str
    filmwork_id: uuid.UUID
    person_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default=datetime.now())


table_dataclass = {
    'content.filmwork': Filmwork,
    'content.genre': Genre,
    'content.genre_filmwork': GenreFilmwork,
    'content.person': Person,
    'content.person_filmwork': PersonFilmwork,
}
