from datetime import date
from uuid import UUID, uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from rental_store.calculator import calculate_rent_charge, calculate_rent_surcharge
from rental_store.orm_classes import Film, Cassette, Customer, RentalRecord, PriceList
from rental_store.data_models import PriceList, \
    FilmRentResponseModel, \
    FilmRentRequestModel, \
    FilmReturnRequestModel, \
    FilmRentResponseItemModel, \
    FilmReturnResponseModel, \
    FilmReturnResponseItemModel, \
    RequestAddFilmModel


class NotAvailableError(Exception):

    def __init__(self, message: str):
        self.message = message


class StoreCheckoutError(Exception):

    def __init__(self, message):
        self.message = message


class StoreCheckout:
    engine = create_engine("postgresql://postgres:password@127.0.0.1:5432/rental_store", echo=True)

    def rent_films(self, rent_request: FilmRentRequestModel) -> FilmRentResponseModel:

        with Session(self.engine) as session:

            try:
                request_id = uuid4()
                stmt = select(Customer).where(Customer.id == rent_request.customer_id)
                customer = session.scalars(stmt).one()

                stmt = select(PriceList)
                price_list = session.scalars(stmt).one()

                response_items = []
                rental_records = []

                for item in rent_request.films_to_rent:

                    stmt = select(Film).where(Film.id == item.film_id)
                    film = session.scalars(stmt).one()

                    try:
                        stmt = select(Cassette).where(Cassette.film_id == item.film_id).where(
                            Cassette.available_flag is True).with_for_update()
                        cassette = session.scalars(stmt).first()
                        cassette.available_flag = False

                    except Exception as e:

                        raise StoreCheckoutError(str(e))

                    charge, currency = calculate_rent_charge(price_list, film, item.up_front_days)

                    new_rental_record = RentalRecord(
                        id=request_id,
                        customer_id=customer.id,
                        cassette_id=cassette.id,
                        up_front_days=item.up_front_days,
                        charge=charge,
                        date_of_rent=date.today())

                    rental_records.append(new_rental_record)

                    response_items.append(FilmRentResponseItemModel(film_id=film.id, charge=charge, currency=currency))

                session.add_all(rental_records)
                session.commit()

                return FilmRentResponseModel(rented_films=response_items)

            except Exception as e:
                raise StoreCheckoutError(str(e))

            except NotAvailableError as e:
                raise StoreCheckoutError(str(e))

    # @staticmethod
    # def return_films(return_request: FilmReturnRequestModel) -> FilmReturnResponseModel:
    #
    #     try:
    #         response_items = []
    #         customer = Repository.get_customer(return_request.customer_id)
    #         ledger = Repository.get_ledger()
    #         price_list = Repository.get_price_list()
    #
    #         for item in return_request.returned_films:
    #
    #             film = Repository.get_film(item.film_id)
    #
    #             for record in ledger.rentals:
    #                 if record.customer_id == customer.id and record.film_id == film.id and record.date_of_return is None:
    #                     surcharge, currency = calculate_rent_surcharge(price_list, film, record.up_front_days,
    #                                                                    record.date_of_rent)
    #
    #                     record.surcharge = surcharge
    #                     record.date_of_return = date.today()
    #
    #                     break
    #
    #             else:
    #                 raise RecordNotFoundError(
    #                     f"Customer id:{customer.id} cannot return film id:{film.id}. "
    #                     f"There is no rental record pending return.")
    #
    #             response_items.append(
    #                 FilmReturnResponseItemModel(film_id=film.id, surcharge=surcharge, currency=currency))
    #
    #             Repository.update_ledger(ledger)
    #
    #             return FilmReturnResponseModel(returned_films=response_items)
    #
    #     except RecordNotFoundError as e:
    #         raise StoreCheckoutError(str(e))

#     @staticmethod
#     def add_customer():
#         return Repository.create_customer()
#
#     @staticmethod
#     def get_customer(customer_id: int):
#
#         try:
#             return Repository.get_customer(customer_id)
#
#         except RecordNotFoundError as e:
#             raise StoreCheckoutError(str(e))
#
#     @staticmethod
#     def get_customers():
#         return {"customers": Repository.get_customers()}
#
#     @staticmethod
#     def load_demo_data():
#         Repository.load_demo_data()
#
#     @staticmethod
#     def get_film_inventory() -> Inventory:
#         return Repository.get_inventory()
#
#     @staticmethod
#     def get_film(film_id: int) -> Inventory:
#         try:
#             return Repository.get_film(film_id)
#
#         except RecordNotFoundError as e:
#             raise StoreCheckoutError(str(e))
#
#     @staticmethod
#     def get_ledger() -> dict:
#         return {"rentals": Repository.get_ledger().rentals}
#
#     @staticmethod
#     def add_film(request: RequestAddFilmModel) -> Film:
#
#         if request.type in Repository.film_types():
#
#             return Repository.create_film(request.title, request.type, request.items_total)
#
#         else:
#             raise StoreCheckoutError(f"Invalid film type: '{request.type}. Valid types are: {Repository.film_types()}.")
#
#
# def reserve_film(ledger: Ledger, request_id: UUID, film: Film):
#     rented = 0
#     for item in ledger.rentals:
#         if item.film_id == film.id and item.date_of_return is None:
#             rented += 1
#
#     reserved = 0
#     for item in ledger.reservations:
#         if item.film_id == film.id:
#             reserved += 1
#
#     available_items = film.items_total - rented - reserved
#
#     if available_items:
#         new_record = ReservationRecord(request_id=request_id, film_id=film.id)
#         ledger.reservations.append(new_record)
#     else:
#         raise NotAvailableError(f"Film id:{film.id}, title: '{film.title}' is not available.")
#
#
# def release_reservation(ledger: Ledger, request_id: UUID):
#     for item in ledger.reservations:
#         if item.request_id == request_id:
#             ledger.reservations.remove(item)
#
#     Repository.update_ledger(ledger)
