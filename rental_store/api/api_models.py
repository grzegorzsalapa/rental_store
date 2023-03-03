from uuid import UUID

from pydantic import BaseModel


# TODO do I need to make it as BaseModel to make it work for rest FastApi
class FilmRentRequestItemModel:
    def __init__(self, film_id: UUID, up_front_days: int):
        self.film_id = film_id
        self.up_front_days = up_front_days


class FilmRentRequestItemModel(BaseModel):
    film_id: UUID
    up_front_days: int


# TODO do I need to make it as BaseModel to make it work for rest FastApi
class FilmRentRequestModel:
    def __init__(self, customer_id: UUID, rented_films: list[FilmRentRequestItemModel]):
        self.customer_id = customer_id
        self.rented_films = rented_films


class RentFilmRequest(BaseModel):
    customer_id: UUID
    rented_films: list[FilmRentRequestItemModel]


class ReturnFilmResponse(BaseModel):
    surcharge: int


class FilmReturnRequest(BaseModel):
    customer_id: UUID
    returned_films: set[UUID]
