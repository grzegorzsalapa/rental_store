from pydantic import BaseModel
from rental_store.data_models import InventoryModel, CustomerModel, Film, Rentals, PriceList, RentalRecordModel
from uuid import uuid4
import datetime


class MemoryDataStorage(BaseModel):

    customers: list[CustomerModel] = []
    inventory: InventoryModel = InventoryModel()
    ledger: Rentals = Rentals()
    price_list: PriceList = PriceList
    film_types: list[str] = ["New release", "Regular", "Old"]

    def load_demo_data(self):
        self.inventory.films = [
            Film(
                id=0,
                title="Matrix 11",
                type="New release",
                items_total=50
            ),
            Film(
                id=1,
                title="Spider Man",
                type="Regular",
                items_total=50
            ),
            Film(
                id=2,
                title="Spider Man 2",
                type="Regular",
                items_total=50
            ),
            Film(
                id=3,
                title="Out of Africa",
                type="Old",
                items_total=50
            )
        ]

        self.customers = [
            CustomerModel(
                id=0,
                rentals=[]
            ),
            CustomerModel(
                id=1,
                rentals=[]
            ),
            CustomerModel(
                id=2,
                rentals=[]
            )
        ]

        self.ledger = Rentals(
            rentals=[
                RentalRecordModel(
                    request_id=uuid4(),
                    film_id=0,
                    customer_id=1,
                    date_of_rent=datetime.date.today() - datetime.timedelta(days=3),
                    up_front_days=1,
                    charge=40
                ),
                RentalRecordModel(
                    request_id=uuid4(),
                    film_id=2,
                    customer_id=0,
                    date_of_rent=datetime.date.today() - datetime.timedelta(days=6),
                    up_front_days=1,
                    charge=90
                ),
                RentalRecordModel(
                    request_id=uuid4(),
                    film_id=3,
                    customer_id=2,
                    date_of_rent=datetime.date.today() - datetime.timedelta(days=5),
                    up_front_days=3,
                    charge=150
                )
            ]
        )

