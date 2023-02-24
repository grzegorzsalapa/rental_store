import rental_store.config
from fastapi import FastAPI, HTTPException
from rental_store.data_models import FilmRentResponseModel, FilmRentRequestModel, FilmReturnRequestModel, FilmReturnResponseModel
from rental_store.data_storage import MemoryDataStorage
from rental_store.store_checkout import rent_films, return_films, get_film_inventory, get_customers_rentals


store = FastAPI()

rental_store.config.data_storage_class = MemoryDataStorage

# data_storage = MemoryDataStorage()


@store.post("/films/rent", response_model=FilmRentResponseModel)
def rent_films(rent_request: FilmRentRequestModel):

    try:
        response = rent_films(rent_request)

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
        response = return_films(return_request)

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
        response = get_film_inventory()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/ledger/{customer_id}")
def get_customers_rentals(customer_id: int):

    return get_customers_rentals(customer_id)
