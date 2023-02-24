import rental_store.config

data_storage = rental_store.config.data_storage_class()


class Repository:

    @classmethod
    def get_customer(cls, customer_id: int):
        pass

    @classmethod
    def get_film_by_id(cls, film_id: int):
        pass

    @classmethod
    def get_film_inventory(cls):
        pass

    @classmethod
    def get_customers_rentals(cls, customer_id: int):
        rentals_ledger = data_storage.get_rentals_ledger

    @classmethod
    def set_reservation_on_film(cls, request_id):
        pass

