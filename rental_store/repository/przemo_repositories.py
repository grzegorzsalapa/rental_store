import datetime
from uuid import UUID
from abc import ABC, abstractmethod
from pydantic import BaseModel
from rental_store.models import Film, Customer


class FilmRentalDetails(BaseModel):
    film_id: UUID  # TODO: should we always set it to None
    rental_date: datetime.date
    charged: int = None  # TODO: change to floating point
    up_front_days: int = None

    def __hash__(self):
        return hash(self.film_id)


class Rental(BaseModel):  # TODO: Do we need BaseModel in here? What other things it give apart from JSON for FastApi()?
    customer_id: UUID
    details: set[FilmRentalDetails] = set()


class RentalsRepository(ABC):
    """An interface for rentals repository"""

    @abstractmethod
    def save(self, rental: Rental):
        raise NotImplementedError()

    @abstractmethod
    def find_by_customer_id(self, customer_id: UUID):
        raise NotImplementedError()


class FilmRepository(ABC):
    """An interface for film repository"""

    @abstractmethod
    def save_film(self, new_film: Film):
        raise NotImplementedError()

    @abstractmethod
    def mark_as_rented(self, film_id: UUID):
        raise NotImplementedError()

    @abstractmethod
    def mark_as_returned(self, film_id: UUID):
        raise NotImplementedError()

    @abstractmethod
    def find_film(self, film_id: UUID) -> Film:
        raise NotImplementedError()


class InMemoryRentalsRepository(RentalsRepository):
    def __init__(self):
        self.rentals: dict[Rental] = dict()

    def save(self, rental: Rental):
        self.rentals[rental.customer_id] = rental

    def find_by_customer_id(self, customer_id: UUID):
        return self.rentals[customer_id]


class InMemoryFilmRepository(FilmRepository):
    def __init__(self):
        self.films: dict[Film] = dict()

    # I Suppose it will add or update
    def save_film(self, new_film):
        self.films[new_film.id] = new_film

    def mark_as_rented(self, film_id):
        film = self.films[film_id]
        film.available_items -= 1

    def mark_as_returned(self, film_id):
        film = self.films[film_id]
        film.available_items += 1

    def find_film(self, film_id) -> Film:
        return self.films[film_id]


class InMemoryCustomerRepository:
    customers: dict[Customer] = dict()

    # I Suppose it will add or update
    def save(self, customer):
        self.customers[customer.id] = customer
