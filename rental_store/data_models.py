from pydantic import BaseModel
from typing import Optional
from enum import IntEnum
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


class FilmModel(BaseModel):
    id: int
    title: str
    type: str
    # items_total: int
    # available_items: Optional[int]


class InventoryModel(BaseModel):
    films: list[FilmModel] = []


class CustomerModel(BaseModel):
    id: int
    # rentals: Optional[list[RentalRecord]]


class PriceList:
    premium_price: int = 40
    basic_price: int = 30


class FilmType(IntEnum):
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
    cassette_id: UUID


class FilmReturnRequestModel(BaseModel):
    customer_id: UUID
    returned_cassettes: list[FilmReturnRequestItemModel]


class FilmRentResponseItemModel(BaseModel):
    film_id: UUID
    cassette_id: UUID
    charge: int
    currency: str


class FilmRentResponseModel(BaseModel):
    rented_films: list[FilmRentResponseItemModel]


class FilmReturnResponseItemModel(BaseModel):
    film_id: UUID
    cassette_id: UUID
    surcharge: int
    currency: str


class FilmReturnResponseModel(BaseModel):
    returned_films: list[FilmReturnResponseItemModel]


class RequestAddFilmModel(BaseModel):
    title: str
    type: str
    items_total: int
