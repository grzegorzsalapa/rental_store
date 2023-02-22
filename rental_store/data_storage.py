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
        self.film_types = []
        self.film_price_list = []

    def add_client_and_set_id(self):
        pass

    def get_client(self):
        pass

    def add_client_rented_items(self):
        pass

    def add_film_types(self, film_types: list):
        pass

    def get_film_types(self):
        pass

    def add_film_to_inventory(self, films: list):
        pass

    def get_all_films(self):
        pass

    def get_film(self, film_ids: list):
        pass

    def create_client_and_set_id(self):
        pass
