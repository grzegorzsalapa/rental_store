import pytest
from unittest.mock import MagicMock, patch
from rental_store.data_interface import FilmRentRequest, FilmRentRequestItem, FilmRentResponse, FilmRentResponseItem
from rental_store.store_checkout import StoreCheckout



def test_rent_films_assignes_film_to_customer_in_rental_ledger():

    def arrangement():
        def _set_up_mocked_repository():
            repository_mock = MagicMock(name="Repository_Instance")
            repository_mock.add_client_and_set_id = MagicMock(return_value=0)
            repository_mock.get_client = MagicMock(return_value=0)
            repository_mock.add_client_rented_items = MagicMock()
            repository_mock.add_item_types = MagicMock()
            repository_mock.get_item_types = MagicMock()
            repository_mock.add_items_to_inventory = MagicMock()
            repository_mock.get_all_items_from_inventory = MagicMock()
            repository_mock.get_items_from_inventory = MagicMock()

            return repository_mock

        repository_mock = _set_up_mocked_repository()

        rent_request = FilmRentRequest(
            customer_id=0,
            rented_films=[
                FilmRentRequestItem(
                    film_id=0,
                    up_front_days=1
                )
            ]
        )

        return repository_mock, rent_request

    def action(repository_mock, rent_request):

        store_checkout = StoreCheckout(repository_mock)
        result = store_checkout.rent_films(rent_request)

        return result

    def assertion(result):

        film_rent_response = FilmRentResponse(
            rented_films=[
                FilmRentResponseItem(
                    film_id=0,
                    charge=40,
                    currency="SEK"
                )
            ]
        )

        assert result == film_rent_response

    repository_mock, rent_request = arrangement()
    with patch('rental_store.store_checkout.calculate_rent_charge', return_value=(40, "SEK")):
        result = action(repository_mock, rent_request)
        assertion(result)