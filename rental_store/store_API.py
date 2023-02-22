from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import date
from rental_store.data_storage import MemoryDataStorage
from rental_store.inventory import FilmInventory
from rental_store.calculators import ChargeCalculatorSelector
from rental_store.client import Client


store = FastAPI()

data_storage = MemoryDataStorage()


class RentListModel(BaseModel):
    film_id: int
    up_front_days: int


class RentRequest(BaseModel):
    client_id: int
    rented_films: list[RentListModel]


@store.post("/films/rent")
def rent_films(rent_request: RentRequest):

    print(rent_request.dict())
    print(rent_request.client_id)
    print(rent_request.rented_films[0].film_id)
    print(rent_request.rented_films[0].up_front_days)

    film_inventory = FilmInventory(data_storage)
    client = Client(rent_request.client_id)
    response_details = []

    for item in rent_request.rented_films:
        film = film_inventory.get_by_id(item.film_id)
        calculator = ChargeCalculatorSelector(film)
        charge, currency = calculator.calculate_rent_charge(item.up_front_days)
        client.rents(film, item.up_front_days, charge, date.today())
        response_details.append({"film_id": film.id, "charge": charge, "currency": currency})

    return response_details


@store.post("/films/return")
def return_films():
    pass


@store.get("/films")
def get_films():
    film_inventory = FilmInventory(data_storage)

    return film_inventory.get_all()
