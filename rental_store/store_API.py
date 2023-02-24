from fastapi import FastAPI, HTTPException
from rental_store.data_interface import FilmRentResponseModel, FilmRentRequestModel, FilmReturnRequestModel, FilmReturnResponseModel
from rental_store.store_checkout import StoreCheckout
from rental_store.data_storage import MemoryDataStorage


store = FastAPI()

store_checkout = StoreCheckout(MemoryDataStorage)


@store.post("/films/rent", response_model=FilmRentResponseModel)
def rent_films(rent_request: FilmRentRequestModel):

    try:
        response = store_checkout.rent_films(rent_request)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.post("/films/return", response_model=FilmReturnResponseModel)
def return_films(return_request: FilmReturnRequestModel):

    try:
        response = store_checkout.return_films(return_request)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/films")
def get_film_inventory():

    try:
        response = store_checkout.get_film_inventory()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/ledger/{customer_id}")
def get_customers_rentals(customer_id: int):

    return store_checkout.get_customers_rentals(customer_id)
