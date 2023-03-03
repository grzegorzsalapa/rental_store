from uuid import UUID

from pydantic import BaseModel


class FilmRentRequestItemModel:
    def __init__(self, film_id: UUID, up_front_days: int):
        self.film_id = film_id
        self.up_front_days = up_front_days


class FilmRentRequestModel:
    def __init__(self, customer_id: UUID, rented_films: list[FilmRentRequestItemModel]):
        self.customer_id = customer_id
        self.rented_films = rented_films


class ReturnFilmResponse(BaseModel):
    surcharge: int


class FilmReturnRequest(BaseModel):
    customer_id: UUID
    returned_films: set[UUID]
