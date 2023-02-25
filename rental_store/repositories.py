import rental_store.config
from rental_store.data_models import Film, Customer


data_storage = rental_store.config.data_storage_class()


class Repository:

    @classmethod
    def get_customer(cls, customer_id: int):
        pass

    @classmethod
    def get_film_by_id(cls, film_id: int) -> Film:
        pass

    @classmethod
    def get_film_inventory(cls):
        pass

    @classmethod
    def get_customers_rentals(cls, customer_id: int):
        rentals_ledger = data_storage.read_rentals_ledger

    @classmethod
    def set_reservation_on_film(cls, film_id: int, request_id):
        data_storage.update_reservetion_list(film_id, request_id)

    @classmethod
    def clear_reservation(cls, request_id):
        pass

    @classmethod
    def clear_reservation_on_film(cls, request_id, film_id):
        pass

