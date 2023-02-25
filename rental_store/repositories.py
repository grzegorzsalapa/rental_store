import rental_store.config
from rental_store.data_models import Film, Customer, Inventory, PriceList, Ledger


data_storage = rental_store.config.data_storage_class()


class Repository:

    @classmethod
    def create_customer(cls, customer_id: int) -> Customer:
        pass

    @classmethod
    def create_film(cls, customer_id: int) -> Film:
        pass

    @classmethod
    def create_inventory(cls) -> Inventory:
        pass

    @classmethod
    def create_price_list(cls) -> PriceList:
        pass

    @classmethod
    def create_ledger(cls) -> Ledger:
        pass

    @classmethod
    def get_customer(cls, customer_id: int) -> Customer:
        pass

    @classmethod
    def get_film(cls, film_id: int) -> Film:
        pass

    @classmethod
    def get_inventory(cls) -> Inventory:
        pass

    @classmethod
    def get_price_list(cls) -> PriceList:
        pass

    @classmethod
    def get_ledger(cls) -> Ledger:
        pass

    @classmethod
    def update_customer(cls, customer: Customer):
        pass

    @classmethod
    def update_film(cls, film: Film):
        pass

    @classmethod
    def update_inventory(cls, inventory: Inventory):
        pass

    @classmethod
    def update_price_list(cls, price_list: PriceList):
        pass

    @classmethod
    def update_ledger(cls, ledger: Ledger):
        pass
