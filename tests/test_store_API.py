import pytest
from fastapi.testclient import TestClient
from rental_store.store_API import store
from unittest.mock import patch, MagicMock
from rental_store.data_interface import FilmRentResponse, FilmRentResponseItem, FilmReturnResponse,\
    FilmReturnResponseItem, FilmInventoryModel, FilmInventoryItemModel


test_client = TestClient(store)


def test_api_rents_films_and_returns_charge():

    def arrangement():
        film_rent_response_item = [FilmRentResponseItem(film_id=0, charge=40, currency="SEK")]
        film_rent_response_mock = FilmRentResponse(rented_films=film_rent_response_item)

        return film_rent_response_mock

    def action():
        response = test_client.post(
            "/films/rent",
            json={
                "client_id": 0,
                "rented_films": [
                    {
                        "film_id": 0,
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
                    "film_id": 0,
                    "charge": 40,
                    "currency": "SEK"
                }
            ]
        }

    with patch('rental_store.store_API.FilmRentResponse', return_value=arrangement()):
        action_result = action()
        assertion(action_result)


def test_api_returns_films_and_returns_surcharge():

    def arrangement():
        film_return_response_item = [FilmReturnResponseItem(film_id=3, surcharge=30, currency="SEK")]
        film_return_response_mock = FilmReturnResponse(returned_films=film_return_response_item)

        return film_return_response_mock

    def action():
        response = test_client.post(
            "/films/return",
            json={
                "client_id": "0",
                "returned_films": [
                    {
                        "film_id": "3"
                    }
                ]
            }
        )
        return response

    def assertion(response):
        assert response.json() == {
            "returned_films": [
                {
                    'film_id': 3,
                    'surcharge': 30,
                    'currency': 'SEK'
                }
            ]
        }

    with patch('rental_store.store_API.FilmReturnResponse', return_value=arrangement()):
        action_result = action()
        assertion(action_result)


def test_api_returns_all_films():

    def arrangement():
        film_inventory_item_1 = FilmInventoryItemModel(film_id=0, film_title="Matrix 11", film_type="New release")
        film_inventory_item_2 = FilmInventoryItemModel(film_id=1, film_title="Spider Man", film_type="Regular")
        film_inventory_mock = FilmInventoryModel(film_inventory=[film_inventory_item_1, film_inventory_item_2])

        return film_inventory_mock

    def action():
        response = test_client.get("/films")

        return response

    def assertion(response):
        assert response.json() == {
            "film_inventory": [
                {
                    "film_id": 0,
                    "film_title": "Matrix 11",
                    "film_type": "New release"
                 },
                {
                    "film_id": 1,
                    "film_title": "Spider Man",
                    "film_type": "Regular"
                 }
            ]
        }

    with patch('rental_store.store_API.FilmInventoryModel', return_value=arrangement()):
        action_result = action()
        assertion(action_result)
