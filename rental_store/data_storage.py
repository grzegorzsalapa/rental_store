from abc import ABC


class DataStorage(ABC):
    pass


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MemoryDataStorage(metaclass=SingletonMeta):

    def __init__(self):
        self.clients = [[], []]
        self.film_inventory = []
        self.film_types = {"New release", "Regular films", "Old films"}
        self.film_price_list = {
            {
                "premium price": 40,
                "currency": "SEK"
            },
            {
                "basic price": 30,
                "currency": "SEK"
            }
        }

    def add_film_types(self, film_types: set):
        self.film_types.update(film_types)

    def get_film_types(self) -> set:
        return self.film_types

    def add_film_to_inventory(self, film: dict):
        pass

    def get_all_films(self):
        pass

    def get_film(self, film_id: int):
        pass

    def create_client_and_set_id(self):
        new_id = len(self.clients[0])
        self.clients[0].append(new_id)
        self.clients[1].append([])

        return new_id

    def add_film_to_clients_ledger(self, film_id: int, up_front_days: int, charge, date_of_rent):
        pass

    def mark_film_as_returned_in_clients_ledger(self, film_id, surcharge, date_of_return):
        pass
