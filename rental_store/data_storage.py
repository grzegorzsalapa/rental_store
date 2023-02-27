from pydantic import BaseModel
from rental_store.data_models import Inventory, Customer, Film, Ledger, PriceList


class MemoryDataStorage(BaseModel):

    customers: list[Customer] = []
    inventory: Inventory = Inventory()
    ledger: Ledger = Ledger()
    price_list: PriceList = PriceList()

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


