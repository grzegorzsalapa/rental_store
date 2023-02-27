from rental_store.data_models import Film, Customer, Inventory, PriceList, Ledger, RentalRecord
from rental_store.data_storage import MemoryDataStorage


data_storage = MemoryDataStorage()


class NotFoundError(Exception):

    def __init__(self, message: str):
        self.message = message


class Repository:

    @classmethod
    def create_customer(cls) -> Customer:
        new_id = 0
        for customer in data_storage.customers:
            new_id = max(new_id, customer.id) + 1

        new_customer = Customer(id=new_id, rentals=[])
        data_storage.customers.append(new_customer)

        return new_customer

    @classmethod
    def create_film(cls) -> Film:
        pass

    @classmethod
    def get_customer(cls, customer_id: int) -> Customer:

        for customer in data_storage.customers:
            if customer.id == customer_id:
                rentals_ledger = data_storage.ledger.rentals
                for record in rentals_ledger:
                    if record.customer_id == customer_id:
                        customer.rentals.append(record)

                return customer

        else:
            raise NotFoundError(f"There is no record of customer id: {customer_id}.")

        return customer

    @classmethod
    def get_film(cls, film_id: int) -> Film:
        inventory = data_storage.inventory
        for film in inventory.films:
            if film.id == film_id:
                return film

        else:
            raise NotFoundError(f"There is no film id: {film_id} in repository.")

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
        data_storage.inventory = inventory

    @classmethod
    def update_price_list(cls, price_list: PriceList):
        data_storage.price_list = price_list

    @classmethod
    def update_ledger(cls, ledger: Ledger):
        data_storage.ledger = ledger

    @classmethod
    def load_demo_data(cls):
        data_storage.load_demo_data()
