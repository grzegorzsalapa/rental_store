from pydantic import BaseModel


class Customer:

    def __init__(self, customer_id: int, rentals: list):
        self.customer_id = customer_id
        self.rentals = rentals

    @property
    def rent_ledger(self) -> list:
        return self.rentals

    @property
    def id(self) -> int:
        return self.customer_id


class Film:

    def __init__(self, film_id, film_title, film_type):
        self.film_id = film_id
        self.film_title = film_title
        self.film_type = film_type

    @property
    def id(self):
        return self.film_id

    @property
    def title(self):
        return self.film_title

    @property
    def type(self):
        return self.film_type


class PriceList:

    def __init__(self, currency, premium_price, basic_price):
        self.currency = currency
        self.premium_price = premium_price
        self.basic_price = basic_price


class FilmRentRequestItemModel(BaseModel):
    film_id: int
    up_front_days: int


class FilmRentRequestModel(BaseModel):
    customer_id: int
    rented_films: list[FilmRentRequestItemModel]


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


class FilmInventoryItemModel(BaseModel):
    film_id: int
    film_title: str
    film_type: str


class FilmInventoryModel(BaseModel):
    film_inventory: list[FilmInventoryItemModel]
