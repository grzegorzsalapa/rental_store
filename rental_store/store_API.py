from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import date
from rental_store.data_storage import MemoryDataStorage
from rental_store.inventory import FilmInventory
from rental_store.calculators import PriceCalculator
from rental_store.client import Client


store = FastAPI()

data_storage = MemoryDataStorage()
price_calculator = PriceCalculator()


class RentListModel(BaseModel):
    film_id: int
    up_front_days: int


class RentRequest(BaseModel):
    client_id: int
    rented_films: list[RentListModel]


@store.post("/films/rent")
def rent_films(rent_request: RentRequest):

    film_inventory = FilmInventory(data_storage)
    client = Client(data_storage, rent_request.client_id)
    response_details = []

    for item in rent_request.rented_films:
        film = film_inventory.get_by_id(item.film_id)
        charge, currency = price_calculator.calculate_rent_charge(film, item.up_front_days)
        client.rents(film, item.up_front_days, charge, date.today())
        response_details.append({"film_id": film.film_id, "charge": charge, "currency": currency})

    return response_details


@store.post("/films/return")
def return_films():
    pass


@store.get("/films")
def get_films():
    film_inventory = FilmInventory(data_storage)

    return film_inventory.get_all()

@store.post("/demo")
def demo():
    for i in range(10):
        Client(data_storage)
