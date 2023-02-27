from datetime import date
from rental_store.calculator import calculate_rent_charge, calculate_rent_surcharge
from rental_store.repositories import Repository, RecordNotFoundError
from rental_store.data_models import Inventory, ReservationRecord, RentalRecord, Ledger, \
    FilmRentResponseModel,\
    FilmRentRequestModel,\
    FilmReturnRequestModel,\
    FilmRentResponseItemModel, \
    FilmReturnResponseModel,\
    FilmReturnResponseItemModel
from uuid import UUID, uuid4


class NotAvailableError(Exception):

    def __init__(self, message: str):
        self.message = message


class StoreCheckoutError(Exception):

    def __init__(self, message):
        self.message = message


class StoreCheckout:

    @staticmethod
    def rent_films(rent_request: FilmRentRequestModel) -> FilmRentResponseModel:

        try:
            request_id = uuid4()
            customer = Repository.get_customer(rent_request.customer_id)
            ledger = Repository.get_ledger()

            for item in rent_request.rented_films:

                try:
                    reserve_film(ledger, request_id, item.film_id)

                except NotAvailableError as e:

                    raise StoreCheckoutError(str(e))

            Repository.update_ledger(ledger)

            price_list = Repository.get_price_list()
            response_items = []

            for item in rent_request.rented_films:

                film = Repository.get_film(item.film_id)

                charge, currency = calculate_rent_charge(price_list, film, item.up_front_days)

                new_rental_record = RentalRecord(
                    request_id=request_id,
                    customer_id=customer.id,
                    film_id=film.id,
                    up_front_days=item.up_front_days,
                    charge=charge,
                    date_of_rent=date.today())

                ledger.rentals.append(new_rental_record)

                response_items.append(FilmRentResponseItemModel(film_id=film.id, charge=charge, currency=currency))

            release_reservation(ledger, request_id)
            Repository.update_ledger(ledger)

            return FilmRentResponseModel(rented_films=response_items)

        except RecordNotFoundError as e:
            raise StoreCheckoutError(str(e))

        except NotAvailableError as e:
            raise StoreCheckoutError(str(e))

    @staticmethod
    def return_films(return_request: FilmReturnRequestModel) -> FilmReturnResponseModel:

        try:
            response_items = []
            ledger = Repository.get_ledger()
            customer = Repository.get_customer(return_request.customer_id)
            price_list = Repository.get_price_list()

            for item in return_request.returned_films:

                film = Repository.get_film(item.film_id)

                for record in ledger.rentals:
                    if record.customer_id == customer.id and record.film_id == film.id and record.date_of_return is None:

                        surcharge, currency = calculate_rent_surcharge(price_list, film, record.up_front_days,
                                                                       record.date_of_rent)

                        record.surcharge = surcharge
                        record.date_of_return = date.today()

                        break

                else:
                    raise RecordNotFoundError(
                        f"Customer id:{customer.id} cannot return film id:{film.id}. "
                        f"There is no rental record pending return.")

                response_items.append(FilmReturnResponseItemModel(film_id=film.id, surcharge=surcharge, currency=currency))

                Repository.update_ledger(ledger)

                return FilmReturnResponseModel(returned_films=response_items)

        except RecordNotFoundError as e:
            raise StoreCheckoutError(str(e))

    @staticmethod
    def add_customer():
        return Repository.create_customer()

    @staticmethod
    def get_customer(customer_id: int):
        return Repository.get_customer(customer_id)

    @staticmethod
    def get_customers():
        return {"customers": Repository.get_customers()}

    @staticmethod
    def load_demo_data():
        Repository.load_demo_data()

    @staticmethod
    def get_film_inventory() -> Inventory:
        return Repository.get_inventory()

    @staticmethod
    def get_ledger() -> dict:
        return {"rentals": Repository.get_ledger().rentals}

    @staticmethod
    def get_customers_rentals(customer_id: int) -> list:
        customer = Repository.get_customer(customer_id)
        return customer.rentals


def reserve_film(ledger: Ledger, request_id: UUID, film_id: int):

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
    else:
        raise NotAvailableError(f"Film id:{film.id}, title: {film.title} is not available.")


def release_reservation(ledger: Ledger, request_id: UUID):

    for item in ledger.reservations:
        if item.request_id == request_id:
            ledger.reservations.remove(item)

    Repository.update_ledger(ledger)


