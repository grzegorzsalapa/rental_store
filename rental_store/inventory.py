from rental_store.repository_interface import RepositoryInterface
from rental_store.data_storage import Film


class FilmInventory:

    def __init__(self, data_storage: RepositoryInterface):
        self.data_storage = data_storage

    def add(self, film: Film):
        self.data_storage.add_film_to_inventory(film)

    def remove(self, film_id: int):
        pass

    def get_by_id(self, film_id: int) -> Film:
        return self.data_storage.get_film_from_inventory(film_id)

    def get_all(self):
        return self.data_storage.get_all_films_from_inventory()


class FilmTypes:

    def __init__(self, data_storage: RepositoryInterface):
        self.data_storage = data_storage

    def add(self, film_types: set):
        self.data_storage.add_item_types(film_types)

    def get_all(self) -> set:
        return self.data_storage.get_item_types()


class FilmPriceList:

    def __init__(self, data_storage: RepositoryInterface):
        self.data_storage = data_storage

    def update(self):
        pass

    def current(self):
        pass
