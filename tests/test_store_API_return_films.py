import pytest
import rental_store.repositories
from fastapi.testclient import TestClient
from rental_store.store_api import store
from rental_store.data_models import Inventory, Film, Customer, PriceList, RentalRecord
from uuid import uuid4
from datetime import date, timedelta


test_client = TestClient(store)


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
