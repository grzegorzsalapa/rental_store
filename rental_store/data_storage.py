from rental_store.data_interface import DataStorageInterface, Film, RentLedger


class MemoryDataStorage(DataStorageInterface):

    def __init__(self):
        self.clients_ledgers = [[], []]
        self.film_inventory = [
            {
                "film_id": 0,
                "film_title": "Matrix 11",
                "film_type": "New release",
             },
            {
                "film_id": 1,
                "film_title": "Spider Man",
                "film_type": "Regular",
             },
            {
                "film_id": 2,
                "film_title": "Spider Man 2",
                "film_type": "Regular",
             },
            {
                "film_id": 3,
                "film_title": "Out of Africa",
                "film_type": "Old",
             }
        ]
        self.film_types = {"New release", "Regular", "Old"}
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

    def get_all_films_from_inventory(self) -> list:
        return self.film_inventory

    def get_film_from_inventory(self, film_id: int) -> Film:
        for item in self.film_inventory:
            if item["film_id"] == film_id:
                film = Film(*[value for value in item.values()])

        return film

    def create_client_and_set_id(self):
        new_id = len(self.clients_ledgers)
        self.clients_ledgers.append([])

        return new_id

    def add_film_to_clients_ledger(self, client_id: int, film: Film, up_front_days: int, charge, date_of_rent):
        self.clients_ledgers[client_id].append(
            {
                "film_id": film.film_id,
                "up_front_days": up_front_days,
                "charge": charge,
                "date_of_rent": date_of_rent
            }
        )

    def mark_film_as_returned_in_clients_ledger(self, client_id: int, film: Film, surcharge, date_of_return):
        for item in self.clients_ledgers[client_id]:
            if item["film_id"] == film.film_id and "date_of_return" not in item.keys():
                item.update(
                    {
                        "surcharge": surcharge,
                        "date_of_return": date_of_return
                    }
                )

    def get_clients_rent_ledger(self, client_id: int) -> RentLedger:
        return self.clients_ledgers[client_id]
