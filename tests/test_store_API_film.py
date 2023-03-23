import pytest
import rental_store.repositories
from fastapi.testclient import TestClient
from rental_store.store_api import store
from rental_store.data_models import Inventory, Film, RentalRecord
from uuid import uuid4
from datetime import date, timedelta


test_client = TestClient(store)


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
