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
    def get_all_films(self) -> list:
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

    def __init__(self, id_, title, type_):
        self.id_ = id_
        self.title = title
        self.type_ = type_


class MemoryDataStorage(DataStorageInterface):

    def __init__(self):
        self.clients = [[], []]
        self.film_inventory = [
            {
                "id": 0,
                "title": "Matrix 11",
                "type": "New release",
             },
            {
                "id": 1,
                "title": "Spider Man",
                "type": "Regular rental",
             },
            {
                "id": 2,
                "title": "Spider Man 2",
                "type": "Regular rental",
             },
            {
                "id": 3,
                "title": "Out of Africa",
                "type": "Old film",
             }
        ]
        self.film_types = {"New release", "Regular films", "Old films"}
        self.film_price_list = [
            {
                "premium price": 40,
                "currency": "SEK"
            },
            {
                "basic price": 30,
                "currency": "SEK"
            }
        ]

    def add_film_types(self, film_types: set):
        self.film_types.update(film_types)

    def get_film_types(self) -> set:
        return self.film_types

    def update_film_type(self, film_id: int):
        pass

    def add_film_to_inventory(self, film: dict):
        pass

    def get_all_films(self) -> list:
        return self.film_inventory

    def get_film_from_inventory(self, film_id: int) -> Film:
        for item in self.film_inventory:
            if item["id"] == film_id:
                film = Film()

        return film

    def create_client_and_set_id(self):
        new_id = len(self.clients[0])
        self.clients[0].append(new_id)
        self.clients[1].append([])

        return new_id

    def add_film_to_clients_ledger(self, film_id: int, up_front_days: int, charge, date_of_rent):
        pass

    def mark_film_as_returned_in_clients_ledger(self, film_id, surcharge, date_of_return):
        pass
