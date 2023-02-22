from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import date
from rental_store.data_storage import MemoryDataStorage
from rental_store.inventory import FilmInventory
from rental_store.calculators import PriceCalculator
from rental_store.client import Client


store = FastAPI()

data_storage = MemoryDataStorage()
film_inventory = FilmInventory(data_storage)
price_calculator = PriceCalculator()


class RentListModel(BaseModel):
    film_id: int
    up_front_days: int


class RentRequest(BaseModel):
    client_id: int
    rented_films: list[RentListModel]


class ReturnListModel(BaseModel):
    film_id: int


class ReturnRequest(BaseModel):
    client_id: int
    returned_films: list[ReturnListModel]


@store.post("/films/rent")
def rent_films(rent_request: RentRequest):

    response_details = []

    for item in rent_request.rented_films:

        film = film_inventory.get_by_id(item.film_id)
        charge, currency = price_calculator.calculate_rent_charge(film, item.up_front_days)

        client = Client(data_storage, rent_request.client_id)
        client.rents(film, item.up_front_days, charge, date.today())

        response_details.append(
            {
                "film_id": film.film_id,
                "charge": charge,
                "currency": currency
            }
        )

    return response_details


@store.post("/films/return")
def return_films(return_request: ReturnRequest):

    response_details = []

    for item in return_request.returned_films:

        film = film_inventory.get_by_id(item.film_id)
        client = Client(data_storage, return_request.client_id)
        surcharge, currency = price_calculator.calculate_rent_surcharge(film, client)

        client.returns(film, surcharge, date.today())

        response_details.append(
            {
                "film_id": film.film_id,
                "surcharge": surcharge,
                "currency": currency
            }
        )

    return response_details


@store.get("/films")
def get_films():

    return film_inventory.get_all()


@store.get("/ledger/{client_id}")
def get_ledger(client_id: int):

    return Client(data_storage, client_id).rent_ledger


@store.post("/demo")
def demo():
    for i in range(10):
        Client(data_storage)
