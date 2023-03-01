import rental_store.repositories
import pytest
from fastapi.testclient import TestClient
from rental_store.store_api import store
from unittest.mock import patch
from rental_store.data_models import Inventory, Film, Ledger, Customer, PriceList, RentalRecord, \
    FilmRentResponseModel,\
    FilmRentResponseItemModel,\
    FilmReturnResponseModel,\
    FilmReturnResponseItemModel,\
    FilmRentRequestItemModel,\
    FilmRentRequestModel,\
    FilmReturnRequestItemModel,\
    FilmReturnRequestModel
from uuid import uuid4
from datetime import date, timedelta


test_client = TestClient(store)


def test_api_post_rent_films_accepts_json_model_and_returns_correct_json_model():

    def arrangement():

        film_rent_response_item = [FilmRentResponseItemModel(film_id=0, charge=40, currency="SEK")]
        film_rent_response = FilmRentResponseModel(rented_films=film_rent_response_item)

        return film_rent_response

    def action():

        response = test_client.post(
            "/films/rent",
            json={
                "customer_id": 0,
                "rented_films": [
                    {
                        "film_id": 0,
                        "up_front_days": 1
                    }
                ]
            }
        )

        return response

    def assertion(response, rent_films_mock):

        assert response.json() == {
            "rented_films": [
                {
                    "film_id": 0,
                    "charge": 40,
                    "currency": "SEK"
                }
            ]
        }

        rent_films_mock.assert_called_once_with(
            FilmRentRequestModel(
                customer_id=0,
                rented_films=[
                    FilmRentRequestItemModel(
                        film_id=0,
                        up_front_days=1
                    )
                ]
            )
        )

    film_rent_response = arrangement()
    with patch('rental_store.store_api.StoreCheckout.rent_films', return_value=film_rent_response) as rent_films_mock:
        action_result = action()
        assertion(action_result, rent_films_mock)


def test_api_post_return_films_accepts_json_model_and_returns_correct_json_mode():

    def arrangement():

        film_return_response_item = [FilmReturnResponseItemModel(film_id=3, surcharge=30, currency="SEK")]
        film_return_response_mock = FilmReturnResponseModel(returned_films=film_return_response_item)

        return film_return_response_mock

    def action():

        response = test_client.post(
            "/films/return",
            json={
                "customer_id": "0",
                "returned_films": [
                    {
                        "film_id": "3"
                    }
                ]
            }
        )
        return response

    def assertion(response, return_films_mock):

        assert response.json() == {
            "returned_films": [
                {
                    'film_id': 3,
                    'surcharge': 30,
                    'currency': 'SEK'
                }
            ]
        }

        return_films_mock.assert_called_once_with(
            FilmReturnRequestModel(
                customer_id=0,
                returned_films=[
                    FilmReturnRequestItemModel(
                        film_id=3,
                    )
                ]
            )
        )

    film_return_response = arrangement()
    with patch('rental_store.store_api.StoreCheckout.return_films', return_value=film_return_response) as return_films_mock:
        result = action()
        assertion(result, return_films_mock)


def test_api_get_film_inventory_returns_correct_json_model():

    def arrangement():

        item_1 = Film(id=0, title="Matrix 11", type="New release", items_total=50, available_items=12)
        item_2 = Film(id=0, title="Spider Man", type="Regular", items_total=50, available_items=10)
        film_inventory_mock = Inventory(films=[item_1, item_2])

        return film_inventory_mock


    def action():
        response = test_client.get("/films")

        return response

    def assertion(response):
        assert response.json() == {
            'films': [
                {
                    'id': 0,
                    'title': 'Matrix 11',
                    'type': 'New release',
                    'items_total': 50,
                    'available_items': 12
                },
                {
                    'id': 0,
                    'title': 'Spider Man',
                    'type': 'Regular',
                    'items_total': 50,
                    'available_items': 10
                }
            ]
        }

    film_inventory_mock = arrangement()
    with patch('rental_store.store_api.StoreCheckout.get_film_inventory', return_value=film_inventory_mock):
        action_result = action()
        assertion(action_result)


def test_end2end_post_rent_films():

    def arrangement():

        rental_store.repositories.data_storage.customers = [Customer(id=7, rentals=[]), Customer(id=10, rentals=[])]
        rental_store.repositories.data_storage.price_list = PriceList()
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=50)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])


    def action():

        response = test_client.post(
            "/films/rent",
            json={
                "customer_id": 7,
                "rented_films": [
                    {
                        "film_id": 5,
                        "up_front_days": 1
                    }
                ]
            }
        )

        return response

    def assertion(response):

        assert response.json() == {
            "rented_films": [
                {
                    "film_id": 5,
                    "charge": 40,
                    "currency": "SEK"
                }
            ]
        }

    arrangement()
    result = action()
    assertion(result)


def test_end2end_post_return_films():

    def arrangement():
        rental_store.repositories.data_storage.customers = [Customer(id=9, rentals=[]), Customer(id=16, rentals=[])]
        rental_store.repositories.data_storage.price_list = PriceList()
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                film_id=5,
                customer_id=9,
                date_of_rent=date.today() - timedelta(days=3),
                up_front_days=1,
                charge=40
            )
        ]
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=50)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])

    def action():

        response = test_client.post(
            "/films/return",
            json={
                "customer_id": "9",
                "returned_films": [
                    {
                        "film_id": "5"
                    }
                ]
            }
        )
        return response

    def assertion(response):

        assert response.json() == {
            "returned_films": [
                {
                    'film_id': 5,
                    'surcharge': 80,
                    'currency': 'SEK'
                }
            ]
        }

    arrangement()
    result = action()
    assertion(result)


def test_end2end_get_film_inventory():

    def arrangement():

        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=1, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                film_id=1,
                customer_id=9,
                date_of_rent=date.today() - timedelta(days=8),
                up_front_days=3,
                charge=120
            )
        ]

    def action():
        response = test_client.get("/films")

        return response

    def assertion(response):
        assert response.json() == {
            'films': [
                {
                    'id': 0,
                    'title': 'Matrix 11',
                    'type': 'New release',
                    'items_total': 50,
                    'available_items': 50
                },
                {
                    'id': 1,
                    'title': 'Spider Man',
                    'type': 'Regular',
                    'items_total': 20,
                    'available_items': 19
                }
            ]
        }

    arrangement()
    action_result = action()
    assertion(action_result)


def test_404_on_post_rent_unavailable_film():

    def arrangement():

        rental_store.repositories.data_storage.customers = [Customer(id=4), Customer(id=7), Customer(id=9)]
        rental_store.repositories.data_storage.price_list = PriceList()
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                customer_id=4,
                film_id=5,
                date_of_rent=date.today() - timedelta(days=3),
                up_front_days=1,
                charge=40
            ),
            RentalRecord(
                request_id=uuid4(),
                customer_id=9,
                film_id=5,
                date_of_rent=date.today() - timedelta(days=3),
                up_front_days=1,
                charge=40
            )
        ]
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=2)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])


    def action():

        response = test_client.post(
            "/films/rent",
            json={
                "customer_id": 7,
                "rented_films": [
                    {
                        "film_id": 5,
                        "up_front_days": 2
                    }
                ]
            }
        )

        return response

    def assertion(response):

        assert response.status_code == 404

    arrangement()
    result = action()
    assertion(result)


def test_404_on_post_rent_film_not_in_inventory():
    def arrangement():
        rental_store.repositories.data_storage.customers = [Customer(id=4), Customer(id=7), Customer(id=9)]
        rental_store.repositories.data_storage.price_list = PriceList()
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=2)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])

    def action():
        response = test_client.post(
            "/films/rent",
            json={
                "customer_id": 4,
                "rented_films": [
                    {
                        "film_id": 6,
                        "up_front_days": 4
                    }
                ]
            }
        )

        return response

    def assertion(response):
        assert response.status_code == 404

    arrangement()
    result = action()
    assertion(result)


def test_404_on_post_rent_film_non_existing_client():
    def arrangement():
        rental_store.repositories.data_storage.customers = [Customer(id=4), Customer(id=7), Customer(id=9)]
        rental_store.repositories.data_storage.price_list = PriceList()
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=20)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])

    def action():
        response = test_client.post(
            "/films/rent",
            json={
                "customer_id": 6,
                "rented_films": [
                    {
                        "film_id": 5,
                        "up_front_days": 4
                    }
                ]
            }
        )

        return response

    def assertion(response):
        assert response.status_code == 404

    arrangement()
    result = action()
    assertion(result)


def test_404_on_post_return_film_that_was_not_rented():

    def arrangement():
        rental_store.repositories.data_storage.customers = [Customer(id=9), Customer(id=16)]
        rental_store.repositories.data_storage.price_list = PriceList()
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                customer_id=9,
                film_id=8,
                date_of_rent=date.today() - timedelta(days=3),
                up_front_days=1,
                charge=40
            )
        ]
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=50)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])

    def action():

        response = test_client.post(
            "/films/return",
            json={
                "customer_id": "9",
                "returned_films": [
                    {
                        "film_id": "5"
                    }
                ]
            }
        )
        return response

    def assertion(response):

        assert response.status_code == 404

    arrangement()
    result = action()
    assertion(result)


def test_404_on_post_return_film_that_was_not_in_inventory():

    def arrangement():
        rental_store.repositories.data_storage.customers = [Customer(id=9), Customer(id=16)]
        rental_store.repositories.data_storage.price_list = PriceList()
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                customer_id=9,
                film_id=8,
                date_of_rent=date.today() - timedelta(days=3),
                up_front_days=1,
                charge=40
            )
        ]
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=50)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])

    def action():

        response = test_client.post(
            "/films/return",
            json={
                "customer_id": "9",
                "returned_films": [
                    {
                        "film_id": "26"
                    }
                ]
            }
        )
        return response

    def assertion(response):

        assert response.status_code == 404

    arrangement()
    result = action()
    assertion(result)


def test_404_on_post_return_film_non_existing_client():

    def arrangement():
        rental_store.repositories.data_storage.customers = [Customer(id=9), Customer(id=16)]
        rental_store.repositories.data_storage.price_list = PriceList()
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                customer_id=9,
                film_id=8,
                date_of_rent=date.today() - timedelta(days=3),
                up_front_days=1,
                charge=40
            )
        ]
        item_5 = Film(id=5, title="Matrix 11", type="New release", items_total=50)
        item_8 = Film(id=8, title="Spider Man", type="Regular", items_total=50)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_5, item_8])

    def action():

        response = test_client.post(
            "/films/return",
            json={
                "customer_id": "10",
                "returned_films": [
                    {
                        "film_id": "5"
                    }
                ]
            }
        )
        return response

    def assertion(response):

        assert response.status_code == 404

    arrangement()
    result = action()
    assertion(result)