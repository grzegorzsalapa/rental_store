from rental_store.data_models import Film, FilmInventoryModel, FilmInventoryItemModel


class MemoryDataStorage:

    def __init__(self):
        self.customers_ledgers = [[], []]
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

    def add_film_to_inventory(self, film: dict):
        pass

    def get_all_films_from_inventory(self) -> FilmInventoryModel:

        films = self.film_inventory.get_all()
        films_formatted = []
        for item in films:
            films_formatted = FilmInventoryItemModel(**item)

        return FilmInventoryModel(film_inventory=films_formatted)

    def get_film_by_id(self, film_id: int) -> Film:
        for item in self.film_inventory:
            if item["film_id"] == film_id:
                film = Film(*[value for value in item.values()])

        return film

    def add_customer_and_get_id(self):
        new_id = len(self.customers_ledgers)
        self.customers_ledgers.append([])

        return new_id

    def get_customer(self, customer_id):
        pass

    def add_film_to_customers_rentals(self, customer_id: int, film: Film, up_front_days: int, charge, date_of_rent):
        self.customers_ledgers[customer_id].append(
            {
                "film_id": film.film_id,
                "up_front_days": up_front_days,
                "charge": charge,
                "date_of_rent": date_of_rent
            }
        )

    def mark_film_as_returned_in_rentals_ledger(self, customer_id: int, film: Film, surcharge, date_of_return):
        for item in self.customers_ledgers[customer_id]:
            if item["film_id"] == film.film_id and "date_of_return" not in item.keys():
                item.update(
                    {
                        "surcharge": surcharge,
                        "date_of_return": date_of_return
                    }
                )

    def get_customers_rentals(self, customer_id: int):
        return self.customers_ledgers[customer_id]
