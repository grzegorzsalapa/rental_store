from rental_store.data_models import Film


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
