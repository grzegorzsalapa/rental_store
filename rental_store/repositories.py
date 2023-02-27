from rental_store.data_models import Film, Customer, Inventory, PriceList, Ledger, RentalRecord
from rental_store.data_storage import MemoryDataStorage


data_storage = MemoryDataStorage()


class RecordNotFoundError(Exception):

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
    def create_film(cls, title: str, type_: str, items_total: int) -> Film:

        new_id = 0
        for film in data_storage.inventory.films:
            new_id = max(new_id, film.id) + 1

        new_film = Film(id=new_id, title=title, type=type_, items_total=items_total)
        data_storage.inventory.films.append(new_film)

        return new_film

    @classmethod
    def get_customers(cls) -> list[Customer]:

        rentals_ledger = data_storage.ledger.rentals
        customers = data_storage.customers

        for customer in customers:
            for record in rentals_ledger:
                if record.customer_id == customer.id:
                    customer.rentals.append(record)

        return customers

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
            raise RecordNotFoundError(f"There is no record of customer id: {customer_id}.")

    @classmethod
    def get_film(cls, film_id: int) -> Film:
        inventory = data_storage.inventory
        for film in inventory.films:
            if film.id == film_id:

                return film
        else:
            raise RecordNotFoundError(f"There is no film id: {film_id} in inventory.")

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

        for item in data_storage.customers:
            if item.id == customer.id:
                item = customer
                break

    @classmethod
    def update_film(cls, film: Film):

        inventory = data_storage.inventory
        for item in inventory.films:
            if item.id == film.id:
                item = film
                break

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
