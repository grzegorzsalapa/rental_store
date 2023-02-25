import rental_store.repositories
from fastapi import FastAPI, HTTPException
from rental_store.data_models import FilmRentResponseModel, FilmRentRequestModel, FilmReturnRequestModel,\
    FilmReturnResponseModel, Inventory
from rental_store.store_checkout import rent_films, return_films, get_film_inventory, get_customers_rentals


store = FastAPI()

rental_store.repositories.data_storage


@store.post("/films/rent", response_model=FilmRentResponseModel)
def api_rent_films(rent_request: FilmRentRequestModel):

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
def api_return_films(return_request: FilmReturnRequestModel):

    try:
        response = return_films(return_request)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/films", response_model=Inventory)
def api_get_film_inventory():

    try:
        response = get_film_inventory()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/rentals/{customer_id}")
def api_get_customers_rentals(customer_id: int):

    return get_customers_rentals(customer_id)
