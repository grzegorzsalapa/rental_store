import pytest
import rental_store.repositories
from fastapi.testclient import TestClient
from rental_store.store_api import store
from rental_store.data_models import Inventory, Film, Customer, RentalRecord


test_client = TestClient(store)


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
        rental_store.repositories.data_storage.customers = [Customer(id=0), Customer(id=9), Customer(id=16), Customer(id=17)]
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
