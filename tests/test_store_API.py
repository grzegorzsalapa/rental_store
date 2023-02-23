import pytest
from fastapi.testclient import TestClient
from rental_store.store_API import store
from unittest.mock import patch, MagicMock
from rental_store.data_interface import FilmRentResponse, FilmRentResponseItem, FilmReturnResponse,\
    FilmReturnResponseItem


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
        film_inventory_mock = MagicMock()
        film_inventory_mock.get_all = MagicMock(return_value=[
                {
                    "id": 0,
                    "title": "Matrix 11",
                    "type": "New release"
                 },
                {
                    "id": 1,
                    "title": "Spider Man",
                    "type": "Regular rental"
                 }
            ]
        )

        return film_inventory_mock

    def action():
        response = test_client.get("/films")

        return response

    def assertion(response):
        assert response.json() == [
            {
                "id": 0,
                "title": "Matrix 11",
                "type": "New release"
             },
            {
                "id": 1,
                "title": "Spider Man",
                "type": "Regular rental"
             }
        ]

    with patch('rental_store.store_API.film_inventory', new=arrangement()):
        action_result = action()
        assertion(action_result)


def _set_up_mocked_data_storage(client_id=None, client_metadata=None):

    data_storage = MagicMock(name="DataStorage_Instance")
    data_storage.add_client_and_set_id = MagicMock(return_value=client_id)
    data_storage.get_client = MagicMock(return_value=client_metadata)
    data_storage.add_client_rented_items = MagicMock()
    data_storage.add_item_types = MagicMock()
    data_storage.get_item_types = MagicMock()
    data_storage.add_items_to_inventory = MagicMock()
    data_storage.get_all_items_from_inventory = MagicMock()
    data_storage.get_items_from_inventory = MagicMock()

    return data_storage