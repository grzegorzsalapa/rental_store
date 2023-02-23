import pytest
from fastapi.testclient import TestClient
from rental_store.store_API import store
from unittest.mock import patch
from rental_store.data_interface import \
    FilmRentResponse,\
    FilmRentResponseItem,\
    FilmReturnResponse,\
    FilmReturnResponseItem,\
    FilmInventoryModel,\
    FilmInventoryItemModel,\
    FilmRentRequestItem,\
    FilmRentRequest,\
    FilmReturnRequestItem,\
    FilmReturnRequest


test_client = TestClient(store)


def test_api_post_rent_films_accepts_json_model_and_returns_correct_json_model():

    def arrangement():

        film_rent_response_item = [FilmRentResponseItem(film_id=0, charge=40, currency="SEK")]
        film_rent_response_mock = FilmRentResponse(rented_films=film_rent_response_item)

        return film_rent_response_mock

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

    def assertion(response, no_shadow_mock):

        assert response.json() == {
            "rented_films": [
                {
                    "film_id": 0,
                    "charge": 40,
                    "currency": "SEK"
                }
            ]
        }

        no_shadow_mock.assert_called_once_with(
            FilmRentRequest(
                customer_id=0,
                rented_films=[
                    FilmRentRequestItem(
                        film_id=0,
                        up_front_days=1
                    )
                ]
            )
        )

    with patch('rental_store.store_API.store_checkout.rent_films', return_value=arrangement()) as no_shadow_mock:
        action_result = action()
        assertion(action_result, no_shadow_mock)


def test_api_post_return_films_accepts_json_model_and_returns_correct_json_mode():

    def arrangement():

        film_return_response_item = [FilmReturnResponseItem(film_id=3, surcharge=30, currency="SEK")]
        film_return_response_mock = FilmReturnResponse(returned_films=film_return_response_item)

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

    def assertion(response, no_shadow_mock):

        assert response.json() == {
            "returned_films": [
                {
                    'film_id': 3,
                    'surcharge': 30,
                    'currency': 'SEK'
                }
            ]
        }

        no_shadow_mock.assert_called_once_with(
            FilmReturnRequest(
                customer_id=0,
                returned_films=[
                    FilmReturnRequestItem(
                        film_id=3,
                    )
                ]
            )
        )

    with patch('rental_store.store_API.store_checkout.return_films', return_value=arrangement()) as no_shadow_mock:
        action_result = action()
        assertion(action_result, no_shadow_mock)


def test_api_get_film_inventory_returns_correct_json_mode():

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

    with patch('rental_store.store_API.store_checkout.get_film_inventory', return_value=arrangement()):
        action_result = action()
        assertion(action_result)
