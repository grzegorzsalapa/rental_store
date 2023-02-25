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
    def get_customer(cls, customer_id: int) -> Customer:
        customers = data_storage.customers
        for customer in customers:
            if customer.id == customer_id:
                rentals_ledger = data_storage.ledger.rentals
                for record in rentals_ledger:
                    if record.customer_id == customer_id:
                        customer.rentals.append(record)

                return customer


    @classmethod
    def get_film(cls, film_id: int) -> Film:
        inventory = data_storage.inventory
        for film in inventory.films:
            if film.id == film_id:
                return film

    @classmethod
    def get_inventory(cls) -> Inventory:
        return data_storage.inventory

    @classmethod
    def get_price_list(cls) -> PriceList:
        return data_storage.price_list

    @classmethod
    def get_ledger(cls) -> Ledger:
        return data_storage.ledger

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
        data_storage.ledger = ledger
