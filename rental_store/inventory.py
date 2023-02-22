from rental_store.data_storage import MemoryDataStorage


class Film:

    def __init__(self, film_id, title, film_type):
        self.film_id = film_id
        self.title = title
        self.film_type = film_type


class FilmInventory:

    def __init__(self, data_storage: MemoryDataStorage):
        self.data_storage = data_storage

    def add(self, film: Film):
        self.data_storage.add_film_to_inventory(film)

    def remove(self, film_id: int):
        pass

    def get_by_id(self, film_id: int):
        return Film(self.data_storage.get_film_from_inventory(film_id))

    def get_all(self):
        return self.data_storage.get_all_films_from_inventory()


class FilmTypes:

    def __init__(self, data_storage: MemoryDataStorage):
        self.data_storage = data_storage

    def add(self, film_types: list):
        self.data_storage.add_item_types(film_types)

    def all(self):
        return self.data_storage.get_item_types()


class FilmPriceList:

    def __init__(self, data_storage: MemoryDataStorage):
        self.data_storage = data_storage

    def update(self):
        pass

    def current(self):
        pass
