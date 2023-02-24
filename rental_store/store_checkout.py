from datetime import date
from typing import Type
from rental_store.calculator import calculate_rent_charge, calculate_rent_surcharge
from rental_store.data_interface import \
    RepositoryInterface,\
    FilmRentResponse,\
    FilmRentRequest,\
    FilmReturnRequest,\
    FilmRentResponseItem, \
    FilmReturnResponse,\
    FilmReturnResponseItem,\
    FilmInventoryItemModel,\
    FilmInventoryModel,\
    Film,\
    Customer


class AvailabilityError(Exception):

    def __init__(self, message: str):
        self.message = message


class StoreCheckout:

    def __init__(self, Repository: Type[RepositoryInterface]):
        self.repository = Repository()

    def rent_films(self, rent_request: FilmRentRequest):

        response_items = []

        for item in rent_request.rented_films:

            film = self.repository.get_film_by_id(item.film_id)
            charge, currency = calculate_rent_charge(film, item.up_front_days)

            customer = self.repository.get_customer(rent_request.customer_id)
            self.repository.add_record_to_rental_ledger(customer, film, item.up_front_days, charge, date.today())

            response_items.append(FilmRentResponseItem(film_id=film.film_id, charge=charge, currency=currency))

        return FilmRentResponse(rented_films=response_items)

    def return_films(self, return_request: FilmReturnRequest):

        response_items = []

        for item in return_request.returned_films:

            film = self.repository.get_film_by_id(item.film_id)
            customer = self.repository.get_customer(return_request.customer_id)
            surcharge, currency = self.price_calculator.calculate_rent_surcharge(film, customer)

            self.return_film(customer, film, surcharge, date.today())

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

    def rent_film(self, customer: Customer, film: Film, up_front_days: int, charge: int, date_of_rent):
        self.repository.add_film_to_rentals_ledger(customer.id, film.id, up_front_days, charge, date_of_rent)

    def return_film(self, customer: Customer, film: Film, surcharge: int, date_of_return):
        self.repository.mark_film_as_returned_in_rentals_ledger(customer.id, film.id, surcharge, date_of_return)
