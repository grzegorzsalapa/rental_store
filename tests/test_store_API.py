import pytest
from fastapi.testclient import TestClient
from rental_store.store_api import store
from unittest.mock import patch
from uuid import uuid4, UUID
from rental_store.data_models import Inventory, Film, \
    FilmRentResponseModel,\
    FilmRentResponseItemModel,\
    FilmReturnResponseModel,\
    FilmReturnResponseItemModel,\
    FilmRentRequestItemModel,\
    FilmRentRequestModel,\
    FilmReturnRequestItemModel,\
    FilmReturnRequestModel


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
    with patch('rental_store.store_api.rent_films', return_value=film_rent_response) as rent_films_mock:
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
    with patch('rental_store.store_api.return_films', return_value=film_return_response) as return_films_mock:
        result = action()
        assertion(result, return_films_mock)


def test_api_get_film_inventory_returns_correct_json_mode():

    def arrangement():

        item_1 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_2 = Film(id=0, title="Spider Man", type="Regular", items_total=50)
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
                    'items_total': 50
                },
                {
                    'id': 0,
                    'title': 'Spider Man',
                    'type': 'Regular',
                    'items_total': 50
                }
            ]
        }

    film_inventory_mock = arrangement()
    with patch('rental_store.store_api.get_film_inventory', return_value=film_inventory_mock):
        action_result = action()
        assertion(action_result)
