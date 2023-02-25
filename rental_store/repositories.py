from rental_store.data_models import Film, Customer, Inventory, PriceList, Ledger, RentalRecord
from rental_store.data_storage import MemoryDataStorage
from uuid import UUID
import datetime

data_storage = MemoryDataStorage()


class Repository:

    @classmethod
    def create_customer(cls) -> Customer:
        pass

    @classmethod
    def create_film(cls) -> Film:
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
    def create_rental_record(cls, request_id: UUID, customer_id: Customer,
                             film_id: int, up_front_days: int, charge: int,
                             date_of_rent: datetime.date) -> RentalRecord:
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
