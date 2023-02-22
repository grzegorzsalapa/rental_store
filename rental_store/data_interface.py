from abc import ABC, abstractmethod


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
    def add_film_to_inventory(self, film: dict):
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
    def add_film_to_clients_ledger(self, film_id: int, up_front_days: int, charge, date_of_rent):
        pass

    @abstractmethod
    def mark_film_as_returned_in_clients_ledger(self, film_id, surcharge, date_of_return):
        pass


class Film:

    def __init__(self, film_id, film_title, film_type):
        self.film_id = film_id
        self.film_title = film_title
        self.film_type = film_type


class RentLedger:
    pass
