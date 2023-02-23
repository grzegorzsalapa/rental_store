from datetime import date
from rental_store.data_storage import MemoryDataStorage
from rental_store.inventory import FilmInventory
from rental_store.calculator import PriceCalculator
from rental_store.customer import Customer
from rental_store.repository_interface import FilmRentResponse, FilmRentRequest, FilmReturnRequest, FilmRentResponseItem,\
    FilmReturnResponse, FilmReturnResponseItem, FilmInventoryItemModel, FilmInventoryModel


class StoreCheckout:

    def __init__(self):
        self.repository = MemoryDataStorage()
        self.film_inventory = FilmInventory(self.repository)
        self.price_calculator = PriceCalculator()

    def rent_films(self, rent_request: FilmRentRequest):

        response_items = []

        for item in rent_request.rented_films:
            film = self.film_inventory.get_by_id(item.film_id)
            charge, currency = self.price_calculator.calculate_rent_charge(film, item.up_front_days)

            customer = Customer(self.repository, rent_request.customer_id)
            customer.rents(film, item.up_front_days, charge, date.today())

            response_items.append(FilmRentResponseItem(film_id=film.film_id, charge=charge, currency=currency))

        return FilmRentResponse(rented_films=response_items)

    def return_films(self, return_request: FilmReturnRequest):

        response_items = []

        for item in return_request.returned_films:
            film = self.film_inventory.get_by_id(item.film_id)
            customer = Customer(self.repository, return_request.customer_id)
            surcharge, currency = self.price_calculator.calculate_rent_surcharge(film, customer)

            customer.returns(film, surcharge, date.today())
            response_items.append(FilmReturnResponseItem(film_id=film.film_id, surcharge=surcharge, currency=currency))

        return FilmReturnResponse(returned_films=response_items)

    def get_film_inventory(self):

        films = self.film_inventory.get_all()
        films_formatted = []
        for item in films:
            films_formatted = FilmInventoryItemModel(**item)

        return FilmInventoryModel(film_inventory=films_formatted)

    def get_ledger(self, customer_id: int):

        return Customer(self.repository, customer_id).rent_ledger

