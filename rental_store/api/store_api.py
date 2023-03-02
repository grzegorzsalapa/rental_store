from fastapi import FastAPI, HTTPException

import rental_store.repository.repositories
from rental_store.models import FilmRentResponseModel, FilmRentRequestModel, FilmReturnRequestModel, \
    FilmReturnResponseModel, RequestAddFilmModel, Inventory, Film
from rental_store.service.store_checkout import StoreCheckout, StoreCheckoutError

store = FastAPI()

rental_store.repositories.data_storage


@store.post("/films/rent", response_model=FilmRentResponseModel)
def api_rent_films(rent_request: FilmRentRequestModel):
    try:
        response = StoreCheckout.rent_films(rent_request)

    except StoreCheckoutError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"X-Error": "Rent error."}
        )

    except Exception as e:

        print(str(e))

        raise HTTPException(
            status_code=500,
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.post("/films/return", response_model=FilmReturnResponseModel)
def api_return_films(return_request: FilmReturnRequestModel):
    try:
        response = StoreCheckout.return_films(return_request)

    except StoreCheckoutError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"X-Error": "Return error."}
        )

    except Exception as e:

        print(str(e))

        raise HTTPException(
            status_code=500,
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/films", response_model=Inventory)
def api_get_film_inventory():
    try:
        response = StoreCheckout.get_film_inventory()

    except Exception as e:

        print(str(e))

        raise HTTPException(
            status_code=500,
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/films/{film_id}", response_model=Film)
def api_get_film(film_id: int):
    try:
        response = StoreCheckout.get_film(film_id)

    except StoreCheckoutError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"X-Error": "Get film error."}
        )

    except Exception as e:

        print(str(e))

        raise HTTPException(
            status_code=500,
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/store/ledger")
def api_get_ledger():
    return StoreCheckout.get_ledger()


@store.post("/customers/add", status_code=201)
def api_add_customer():
    return StoreCheckout.add_customer()


@store.get("/customers/{customer_id}")
def api_get_customer(customer_id: int):
    try:
        response = StoreCheckout.get_customer(customer_id)

    except StoreCheckoutError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"X-Error": "Get customer error."}
        )

    except Exception as e:

        print(str(e))

        raise HTTPException(
            status_code=500,
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/customers")
def api_get_customers():
    return StoreCheckout.get_customers()


@store.post("/films/add", status_code=201, response_model=Film)
def api_add_film(add_film_request: RequestAddFilmModel):
    try:
        return StoreCheckout.add_film(add_film_request)

    except StoreCheckoutError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"X-Error": "Add film error."}
        )

    except Exception as e:

        print(str(e))

        raise HTTPException(
            status_code=500,
            headers={"X-Error": "Unexpected error."}
        )


@store.post("/demo")
def api_start_demo():
    StoreCheckout.load_demo_data()

    return "Demo data loaded"
