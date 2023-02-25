from pydantic import BaseModel
from rental_store.data_models import Inventory, Customer, Ledger, PriceList


class MemoryDataStorage(BaseModel):

    customers: list[Customer] = []
    inventory: Inventory = Inventory()
    ledger: Ledger = Ledger()
    price_list: PriceList = PriceList()


film_inventory = [
    {
        "film_id": 0,
        "film_title": "Matrix 11",
        "film_type": "New release",
     },
    {
        "film_id": 1,
        "film_title": "Spider Man",
        "film_type": "Regular",
     },
    {
        "film_id": 2,
        "film_title": "Spider Man 2",
        "film_type": "Regular",
     },
    {
        "film_id": 3,
        "film_title": "Out of Africa",
        "film_type": "Old",
     }
]
film_types = {"New release", "Regular", "Old"}

