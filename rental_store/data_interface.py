from abc import ABC, abstractmethod
from pydantic import BaseModel


class Film:

    def __init__(self, film_id, film_title, film_type):
        self.film_id = film_id
        self.film_title = film_title
        self.film_type = film_type


class RentLedger:
    pass


class FilmRentRequestItem(BaseModel):
    film_id: int
    up_front_days: int


class FilmRentRequest(BaseModel):
    client_id: int
    rented_films: list[FilmRentRequestItem]


class FilmReturnRequestItem(BaseModel):
    film_id: int


class FilmReturnRequest(BaseModel):
    client_id: int
    returned_films: list[FilmReturnRequestItem]


class FilmRentResponseItem(BaseModel):
    film_id: int
    charge: int
    currency: str


class FilmRentResponse(BaseModel):
    rented_films: list[FilmRentResponseItem]


class FilmReturnResponseItem(BaseModel):
    film_id: int
    surcharge: int
    currency: str


class FilmReturnResponse(BaseModel):
    returned_films: list[FilmReturnResponseItem]


class DataStorageInterface(ABC):
    @abstractmethod
    def add_film_types(self, film_types: set):
        pass

    @abstractmethod
    def get_film_types(self) -> set:
        pass

    @abstractmethod
    def update_film_type(self, film_id: int):
        pass

    @abstractmethod
    def add_film_to_inventory(self, film: Film):
        pass

    @abstractmethod
    def get_all_films_from_inventory(self) -> list:
        pass

    @abstractmethod
    def get_film_from_inventory(self, film_id: int):
        pass

    @abstractmethod
    def create_client_and_set_id(self):
        pass

    @abstractmethod
    def add_film_to_clients_ledger(self, client_id: int, film: Film, up_front_days: int, charge, date_of_rent):
        pass

    @abstractmethod
    def mark_film_as_returned_in_clients_ledger(self, client_id: int, film: Film, surcharge, date_of_return):
        pass

    @abstractmethod
    def get_clients_rent_ledger(self, client_id: int) -> RentLedger:
        pass
