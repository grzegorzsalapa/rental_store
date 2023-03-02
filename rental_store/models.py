import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RentalRecord(BaseModel):
    request_id: UUID = None
    customer_id: int = None
    film_id: int = None
    date_of_rent: datetime.date = None
    up_front_days: int = None
    charge: int = None
    date_of_return: datetime.date = None
    surcharge: int = None


class ReservationRecord(BaseModel):
    request_id: UUID
    film_id: int


class Ledger(BaseModel):
    rentals: list[RentalRecord] = []
    reservations: list[ReservationRecord] = []


class Film(BaseModel):
    id: UUID
    title: str
    type: str
    items_total: int
    available_items: int


class Inventory(BaseModel):
    films: list[Film] = []


class Customer(BaseModel):
    id: int
    rentals: Optional[list[RentalRecord]]


class PriceList(BaseModel):
    currency: str = "SEK"
    premium_price: int = 40
    basic_price: int = 30


class FilmRentRequestItemModel:
    def __init__(self, film_id: UUID, up_front_days: int):
        self.film_id = film_id
        self.up_front_days = up_front_days


class FilmRentRequestModel:
    def __init__(self, customer_id: UUID, rented_films: list[FilmRentRequestItemModel]):
        self.customer_id = customer_id
        self.rented_films = rented_films


class FilmReturnRequestItemModel(BaseModel):
    film_id: int


class FilmReturnRequestModel(BaseModel):
    customer_id: int
    returned_films: list[FilmReturnRequestItemModel]


class FilmReturnRequest(BaseModel):
    customer_id: UUID
    returned_films: set[UUID]


class ReturnFilmResponse(BaseModel):
    surcharge: int


class FilmRentResponseItemModel(BaseModel):
    film_id: int
    charge: int
    currency: str


class FilmRentResponseModel(BaseModel):
    rented_films: list[FilmRentResponseItemModel]


class FilmReturnResponseItemModel(BaseModel):
    film_id: int
    surcharge: int
    currency: str


class FilmReturnResponseModel(BaseModel):
    returned_films: list[FilmReturnResponseItemModel]


class RequestAddFilmModel(BaseModel):
    title: str
    type: str
    items_total: int
