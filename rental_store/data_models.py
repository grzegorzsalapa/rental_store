from pydantic import BaseModel
from typing import Optional
from enum import Enum
import datetime
from uuid import UUID


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
    id: int
    title: str
    type: str
    items_total: int
    available_items: Optional[int]


class Inventory(BaseModel):
    films: list[Film] = []


class Customer(BaseModel):
    id: int
    rentals: Optional[list[RentalRecord]]


class PriceList:
    premium_price: int = 40
    basic_price: int = 30


class FilmType(Enum):
    NEW_RELEASE = 0
    REGULAR = 1
    OLD = 2


class FilmRentRequestItemModel(BaseModel):
    film_id: UUID
    up_front_days: int


class FilmRentRequestModel(BaseModel):
    customer_id: UUID
    films_to_rent: list[FilmRentRequestItemModel]


class FilmReturnRequestItemModel(BaseModel):
    film_id: int


class FilmReturnRequestModel(BaseModel):
    customer_id: int
    returned_films: list[FilmReturnRequestItemModel]


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
