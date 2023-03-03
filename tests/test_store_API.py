from datetime import date, timedelta
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

import rental_store.repository.repositories
from rental_store.api.store_api import store
from rental_store.models import Inventory, Film, Customer, PriceList, RentalRecord, \
    FilmRentResponseModel, \
    FilmRentResponseItemModel, \
    FilmReturnResponseModel, \
    FilmReturnResponseItemModel, \
    FilmReturnRequestItemModel, \
    FilmReturnRequestModel
from rental_store.api.api_models import FilmRentRequestModel, FilmRentRequestItemModel

test_client = TestClient(store)


def test_api_post_rent_films_accepts_json_model_and_returns_correct_json_model():
    # given
    def arrangement():
        film_rent_response_item = [FilmRentResponseItemModel(film_id=0, charge=40, currency="SEK")]
        film_rent_response = FilmRentResponseModel(rented_films=film_rent_response_item)

        return film_rent_response

    # when
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

    # then
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
    with patch('rental_store.store_api.StoreCheckout.return_films',
               return_value=film_return_response) as return_films_mock:
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
        rental_store.repositories.data_storage.customers = [Customer(id=9), Customer(id=16)]
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


def test_end2end_get_get_film():
    def arrangement():
        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=1, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                customer_id=9,
                film_id=0,
                date_of_rent='2021-07-23',
                up_front_days=3,
                charge=120
            )
        ]

    def action():
        response = test_client.get("/films/0")

        return response

    def assertion(response):
        assert response.json() == {
            'id': 0,
            'title': 'Matrix 11',
            'type': 'New release',
            'items_total': 50,
            'available_items': 49
        }

    arrangement()
    action_result = action()
    assertion(action_result)


def test_end2end_post_add_film():
    def arrangement():

        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=12, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])

    def action():
        response = test_client.post(
            "/films/add",
            json={
                "title": "Film o dupie Maryni",
                "type": "Old",
                "items_total": "5"
            }
        )

        return response

    def assertion(response):

        assert response.json() == {
            "id": 13,
            "title": "Film o dupie Maryni",
            "type": "Old",
            "items_total": 5,
            "available_items": 5
        }

        for film in rental_store.repositories.data_storage.inventory.films:
            if film.id == 13:
                assert film.type == "Old"
                assert film.items_total == 5

                break

        else:
            assert False

    arrangement()
    action_result = action()
    assertion(action_result)


def test_end2end_post_add_customer():
    def arrangement():

        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=12, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])
        rental_store.repositories.data_storage.customers = [Customer(id=9), Customer(id=16)]

    def action():
        response = test_client.post("/customers/add")

        return response

    def assertion(response):

        assert response.json() == {
            "id": 17,
            "rentals": []
        }

        for customer in rental_store.repositories.data_storage.customers:
            if customer.id == 17:
                assert customer.rentals is None

                break

        else:
            assert False

    arrangement()
    action_result = action()
    assertion(action_result)


def test_end2end_get_get_customer():
    def arrangement():
        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=1, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])
        rental_store.repositories.data_storage.customers = [Customer(id=9), Customer(id=16)]
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id='bab7010e-7803-468f-807b-6f4252a57178',
                customer_id=9,
                film_id=1,
                date_of_rent='2023-01-11',
                up_front_days=3,
                charge=120
            )
        ]

    def action():
        response = test_client.get("/customers/9")

        return response

    def assertion(response):
        assert response.json() == {
            'id': 9,
            'rentals': [
                {'request_id': 'bab7010e-7803-468f-807b-6f4252a57178',
                 'customer_id': 9,
                 'film_id': 1,
                 'date_of_rent': '2023-01-11',
                 'up_front_days': 3,
                 'charge': 120,
                 'date_of_return': None,
                 'surcharge': None
                 }
            ]
        }

    arrangement()
    action_result = action()
    assertion(action_result)


def test_end2end_get_customers():
    def arrangement():
        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=1, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])
        rental_store.repositories.data_storage.customers = [Customer(id=0), Customer(id=9), Customer(id=16),
                                                            Customer(id=17)]
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id='bab7010e-7803-468f-807b-6f4252a57178',
                customer_id=9,
                film_id=1,
                date_of_rent='2023-01-11',
                up_front_days=3,
                charge=120
            )
        ]

    def action():
        response = test_client.get("/customers")

        return response

    def assertion(response):
        assert response.json() == {
            'customers': [
                {
                    'id': 0,
                    'rentals': []
                },
                {
                    'id': 9,
                    'rentals': [
                        {
                            'charge': 120,
                            'customer_id': 9,
                            'date_of_rent': '2023-01-11',
                            'date_of_return': None,
                            'film_id': 1,
                            'request_id': 'bab7010e-7803-468f-807b-6f4252a57178',
                            'surcharge': None,
                            'up_front_days': 3
                        }
                    ]
                },
                {
                    'id': 16,
                    'rentals': []
                },
                {
                    'id': 17,
                    'rentals': []
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


def test_404_on_post_rent_film_non_existing_customer():
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


def test_404_on_post_return_film_non_existing_customer():
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


def test_404_on_get_film_not_in_inventory():
    def arrangement():
        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=1, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id=uuid4(),
                customer_id=9,
                film_id=0,
                date_of_rent='2021-07-23',
                up_front_days=3,
                charge=120
            )
        ]

    def action():
        response = test_client.get("/films/2")

        return response

    def assertion(response):
        assert response.status_code == 404

    arrangement()
    action_result = action()
    assertion(action_result)


def test_404_on_get_customer_that_does_not_exist():
    def arrangement():
        item_0 = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        item_1 = Film(id=1, title="Spider Man", type="Regular", items_total=20)
        rental_store.repositories.data_storage.inventory = Inventory(films=[item_0, item_1])
        rental_store.repositories.data_storage.customers = [Customer(id=9), Customer(id=16)]
        rental_store.repositories.data_storage.ledger.rentals = [
            RentalRecord(
                request_id='bab7010e-7803-468f-807b-6f4252a57178',
                customer_id=9,
                film_id=1,
                date_of_rent='2023-01-11',
                up_front_days=3,
                charge=120
            )
        ]

    def action():
        response = test_client.get("/customers/13")

        return response

    def assertion(response):
        assert response.status_code == 404

    arrangement()
    action_result = action()
    assertion(action_result)
