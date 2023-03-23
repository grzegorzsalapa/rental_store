from datetime import date
from uuid import UUID, uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exc
from rental_store.calculator import PriceCalculator
from rental_store.orm_classes import Film, Cassette, Customer, RentalRecord
from rental_store.data_models import CustomerModel, FilmModel, InventoryModel, RentalRecordModel, Rentals, \
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


class RecordNotFoundError(Exception):

    def __init__(self, message: str):
        self.message = message


class StoreCheckoutError(Exception):

    def __init__(self, message):
        self.message = message


class StoreCheckout:

    def __init__(self, price_calculator: PriceCalculator):
        self.price_calculator = price_calculator
        self.engine = create_engine("postgresql://postgres:password@127.0.0.1:5432/rental_store", echo=True)

    def rent_films(self, rent_request: FilmRentRequestModel) -> FilmRentResponseModel:

        request_id = uuid4()

        with Session(self.engine) as session:

            try:
                try:
                    stmt = select(Customer).where(Customer.id == rent_request.customer_id)
                    customer = session.scalars(stmt).one()

                except exc.NoResultFound:
                    raise RecordNotFoundError(f"No record of customer id:{rent_request.customer_id}")

                response_items = []
                rental_records = []

                for item in rent_request.films_to_rent:

                    try:
                        stmt = select(Film).where(Film.id == item.film_id)
                        film: Film = session.scalars(stmt).one()

                    except exc.NoResultFound:
                        raise RecordNotFoundError(f"No record of film id:{item.film_id}.")

                    try:
                        stmt = select(Cassette).where(Cassette.film_id == film.id).where(
                            Cassette.available_flag == True).with_for_update()
                        cassette: Cassette = session.scalars(stmt).first()
                        cassette.available_flag = False

                    except exc.NoResultFound:
                        raise NotAvailableError(f"Film id:{film.id} currently not available.")

                    charge = self.price_calculator.calculate_rent_charge(film.type, item.up_front_days)

                    new_rental_record = RentalRecord(
                        id=request_id,
                        customer_id=customer.id,
                        cassette_id=cassette.id,
                        up_front_days=item.up_front_days,
                        charge=charge,
                        date_of_rent=date.today())

                    rental_records.append(new_rental_record)

                    response_items.append(
                        FilmRentResponseItemModel(film_id=film.id, cassette_id=cassette.id, charge=charge,
                                                  currency="SEK"))

                session.add_all(rental_records)
                session.commit()

                return FilmRentResponseModel(rented_films=response_items)

            except RecordNotFoundError as e:
                raise StoreCheckoutError(str(e))

            except NotAvailableError as e:
                raise StoreCheckoutError(str(e))

    def return_films(self, return_request: FilmReturnRequestModel) -> FilmReturnResponseModel:

        with Session(self.engine) as session:

            try:
                try:
                    response_items = []
                    stmt = select(Customer).where(Customer.id == return_request.customer_id)
                    customer = session.scalars(stmt).one()

                except exc.NoResultFound:
                    raise RecordNotFoundError(f"No record of customer id:{return_request.customer_id}")

                for item in return_request.returned_cassettes:

                    try:
                        stmt = select(Cassette).where(Cassette.id == item.cassette_id)
                        cassette: Cassette = session.scalars(stmt).one()
                        cassette.available_flag = True

                    except exc.NoResultFound:
                        raise RecordNotFoundError(f"No record of cassette id:{item.cassette_id}.")

                    try:
                        stmt = select(RentalRecord).where(RentalRecord.cassette_id == cassette.id).where(
                            RentalRecord.customer_id == customer.id).where(
                            RentalRecord.date_of_return == None).with_for_update()
                        rental_record: RentalRecord = session.scalars(stmt).one()

                    except exc.NoResultFound:
                        raise RecordNotFoundError(
                            f"Customer id:{customer.id} cannot return cassette id:{cassette.id}. "
                            f"There is no rental record pending return.")

                    stmt = select(Film).where(Film.id == cassette.film_id)
                    film: Film = session.scalars(stmt).one()

                    surcharge = self.price_calculator.calculate_rent_surcharge(
                        film.type,
                        rental_record.up_front_days,
                        rental_record.date_of_rent)

                    rental_record.surcharge = surcharge
                    rental_record.date_of_return = date.today()

                    response_items.append(
                        FilmReturnResponseItemModel(film_id=film.id, cassette_id=cassette.id, surcharge=surcharge,
                                                    currency="SEK"))

                session.commit()

                return FilmReturnResponseModel(returned_films=response_items)

            except RecordNotFoundError as e:
                raise StoreCheckoutError(str(e))

    def add_customer(self):

        with Session(self.engine) as session:
            customer = Customer(id=uuid4())
            session.add(customer)
            session.commit()

            return f"/customers/{customer.id}"

    def get_customer(self, customer_id: UUID):

        with Session(self.engine) as session:
            try:
                try:
                    stmt = select(Customer).where(Customer.id == customer_id)
                    customer = session.scalars(stmt).one()

                    return customer

                except exc.NoResultFound:
                    raise RecordNotFoundError(f"No record of customer id:{customer_id}")

            except RecordNotFoundError as e:
                raise StoreCheckoutError(str(e))

    def get_customers(self) -> dict:

        with Session(self.engine) as session:
            stmt = select(Customer)
            customers: [Customer] = session.scalars(stmt).all()
            customer_lst = []

            for customer in customers:
                customer_lst.append(CustomerModel(id=customer.id))

            return {"customers": customer_lst}

    def get_film_inventory(self) -> InventoryModel:

        with Session(self.engine) as session:
            stmt = select(Film)
            films: [Film] = session.scalars(stmt).all()
            inventory = InventoryModel(films=[])
            for film in films:
                inventory.films.append(FilmModel(id=film.id, title=film.title, type=film.type))

            return inventory

    def get_rentals(self) -> Rentals:

        with Session(self.engine) as session:
            stmt = select(RentalRecord)
            rental_records: [RentalRecord] = session.scalars(stmt).all()
            rentals = Rentals()

            for record in rental_records:
                rentals.rentals.append(
                    RentalRecordModel(
                        request_id=record.id,
                        customer_id=record.customer_id,
                        cassette_id=record.cassette_id,
                        date_of_rent=record.date_of_rent,
                        up_front_days=record.up_front_days,
                        charge=record.charge,
                        date_of_return=record.date_of_return,
                        surcharge=record.surcharge
                    )
                )

            return rentals

#     def get_film(film_id: int) -> Inventory:
#         try:
#             return Repository.get_film(film_id)
#
#         except RecordNotFoundError as e:
#             raise StoreCheckoutError(str(e))
#     def add_film(request: RequestAddFilmModel) -> Film:
#
#         if request.type in Repository.film_types():
#
#             return Repository.create_film(request.title, request.type, request.items_total)
#
#         else:
#             raise StoreCheckoutError(f"Invalid film type: '{request.type}. Valid types are: {Repository.film_types()}.")
#
#     def load_demo_data():
#         Repository.load_demo_data()