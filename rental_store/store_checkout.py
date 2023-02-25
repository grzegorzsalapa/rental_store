from datetime import date
from rental_store.calculator import calculate_rent_charge, calculate_rent_surcharge
from rental_store.repositories import Repository
from rental_store.data_models import \
    FilmRentResponseModel,\
    FilmRentRequestModel,\
    FilmReturnRequestModel,\
    FilmRentResponseItemModel, \
    FilmReturnResponseModel,\
    FilmReturnResponseItemModel,\
    FilmInventoryItemModel,\
    FilmInventoryModel,\
    Film,\
    Customer
import uuid


class AvailabilityError(Exception):

    def __init__(self, message: str):
        self.message = message


class RentError(Exception):

    def __init__(self, message):
        self.message = message


def rent_films(rent_request: FilmRentRequestModel) -> FilmRentResponseModel:

    request_id = uuid.uuid4()

    for item in rent_request.rented_films:

        try:
            reserve_film(request_id, item.film_id)

        except AvailabilityError as e:
            Repository.clear_reservation(request_id)

            raise RentError(str(e))

    customer = Repository.get_customer(rent_request.customer_id)
    response_items = []

    for item in rent_request.rented_films:

        film = Repository.get_film_by_id(item.film_id)

        charge, currency = calculate_rent_charge(film, item.up_front_days)

        add_record_to_rental_ledger(request_id, customer.id, film.id, item.up_front_days, charge, date.today())

        response_items.append(FilmRentResponseItemModel(film_id=film.id, charge=charge, currency=currency))

    return FilmRentResponseModel(rented_films=response_items)


def return_films(return_request: FilmReturnRequestModel) -> FilmReturnResponseModel:

    response_items = []

    for item in return_request.returned_films:

        film = Repository.get_film_by_id(item.film_id)
        customer = Repository.get_customer(return_request.customer_id)
        surcharge, currency = calculate_rent_surcharge(film, customer)

        return_film(customer, film, surcharge, date.today())

        response_items.append(FilmReturnResponseItemModel(film_id=film.film_id, surcharge=surcharge, currency=currency))

    return FilmReturnResponseModel(returned_films=response_items)


def get_film_inventory():
    return Repository.get_film_inventory()


def get_customers_rentals(customer_id: int) -> list:
    customer = Repository.get_customer(customer_id)
    return customer.rentals


def reserve_film(request_id, film_id: int):

    film = Repository.get_film_by_id(film_id)
    available_items = film.items_total - len(film.reservation_list)

    if available_items:
        film.reservation_list.append(request_id)
        Repository.update_film(film)
    else:
        raise AvailabilityError(f"Film id:{film.id}, title: {film.title} is not available.")


def add_record_to_rental_ledger(request_id, customer_id, film_id, up_front_days, charge, date_of_rent):
    pass


def return_film(customer: Customer, film: Film, surcharge: int, date_of_return):
    pass


