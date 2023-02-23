from fastapi import FastAPI, HTTPException
from rental_store.data_interface import FilmRentResponse, FilmRentRequest, FilmReturnRequest, FilmReturnResponse
from rental_store.store_checkout import StoreCheckout
from rental_store.data_storage import MemoryDataStorage


store = FastAPI()

store_checkout = StoreCheckout(MemoryDataStorage)


@store.post("/films/rent", response_model=FilmRentResponse)
def rent_films(rent_request: FilmRentRequest):

    try:
        response = store_checkout.rent_films(rent_request)

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=str(e),
                            headers={"X-Error": "Unexpected error."})

    return response


@store.post("/films/return", response_model=FilmReturnResponse)
def return_films(return_request: FilmReturnRequest):

    try:
        response = store_checkout.return_films(return_request)

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=str(e),
                            headers={"X-Error": "Unexpected error."})

    return response


@store.get("/films")
def get_film_inventory():

    try:
        response = store_checkout.get_film_inventory()

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=str(e),
                            headers={"X-Error": "Unexpected error."})

    return response


@store.get("/ledger/{customer_id}")
def get_ledger(customer_id: int):

    return store_checkout.get_ledger(customer_id)
