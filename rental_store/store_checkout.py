from datetime import date
from rental_store.calculator import calculate_rent_charge, calculate_rent_surcharge
from rental_store.repositories import Repository
from rental_store.data_models import Film, Customer, Inventory, ReservationRecord, \
    FilmRentResponseModel,\
    FilmRentRequestModel,\
    FilmReturnRequestModel,\
    FilmRentResponseItemModel, \
    FilmReturnResponseModel,\
    FilmReturnResponseItemModel
from uuid import UUID, uuid4


class AvailabilityError(Exception):

    def __init__(self, message: str):
        self.message = message


class RentError(Exception):

    def __init__(self, message):
        self.message = message


def rent_films(rent_request: FilmRentRequestModel) -> FilmRentResponseModel:

    request_id = uuid4()

    for item in rent_request.rented_films:

        try:
            reserve_film(request_id, item.film_id)

        except AvailabilityError as e:
            release_reservation(request_id)

            raise RentError(str(e))

    customer = Repository.get_customer(rent_request.customer_id)
    response_items = []

    for item in rent_request.rented_films:

        film = Repository.get_film(item.film_id)
        price_list = Repository.get_price_list()

        charge, currency = calculate_rent_charge(price_list, film, item.up_front_days)

        Repository.create_rental_record(request_id, customer, film.id, item.up_front_days, charge, date.today())

        response_items.append(FilmRentResponseItemModel(film_id=film.id, charge=charge, currency=currency))

    release_reservation(request_id)

    return FilmRentResponseModel(rented_films=response_items)


def return_films(return_request: FilmReturnRequestModel) -> FilmReturnResponseModel:

    response_items = []

    for item in return_request.returned_films:

        film = Repository.get_film(item.film_id)
        customer = Repository.get_customer(return_request.customer_id)
        price_list = Repository.get_price_list()

        surcharge, currency = calculate_rent_surcharge(price_list, film, customer)

        return_film(customer, film, surcharge, date.today())

        response_items.append(FilmReturnResponseItemModel(film_id=film.id, surcharge=surcharge, currency=currency))

    return FilmReturnResponseModel(returned_films=response_items)


def get_film_inventory() -> Inventory:
    return Repository.get_inventory()


def get_customers_rentals(customer_id: int) -> list:
    customer = Repository.get_customer(customer_id)
    return customer.rentals


def reserve_film(request_id: UUID, film_id: int):

    ledger = Repository.get_ledger()

    rented = 0
    for item in ledger.rentals:
        if item.film_id == film_id:
            rented += 1

    reserved = 0
    for item in ledger.reservations:
        if item.film_id == film_id:
            reserved += 1

    film = Repository.get_film(film_id)

    available_items = film.items_total - rented - reserved

    if available_items:
        new_record = ReservationRecord(request_id=request_id, film_id=film_id)
        ledger.reservations.append(new_record)
        Repository.update_ledger(ledger)
    else:
        raise AvailabilityError(f"Film id:{film.id}, title: {film.title} is not available.")


def release_reservation(request_id):

    ledger = Repository.get_ledger()
    for item in ledger.reservations:
        if item.request_id == request_id:
            ledger.reservations.remove(item)

    Repository.update_ledger(ledger)


def add_record_to_ledger(request_id: UUID, customer_id: Customer, film_id, up_front_days, charge, date_of_rent):
    pass


def return_film(customer: Customer, film: Film, surcharge: int, date_of_return):
    pass


