import pytest
from unittest.mock import MagicMock, patch
from rental_store.data_interface import \
    FilmRentRequest,\
    FilmRentRequestItem,\
    FilmRentResponse,\
    FilmRentResponseItem,\
    Film,\
    Customer
from rental_store.store_checkout import StoreCheckout, AvailabilityError


def test_rent_films_assignes_film_to_customer_in_rental_ledger():

    def arrangement():
        def _set_up_mocked_repository():
            repository_mock = MagicMock(name="Repository_Instance")
            repository_mock.get_film_by_id = MagicMock(return_value=Film(0, "Matrix 11", "New release"))
            repository_mock.get_customer = MagicMock(resturn_value=Customer(700, rentals=[]))
            repository_mock.reserv_film = MagicMock()
            repository_mock.add_record_to_rental_ledger = MagicMock()

            return repository_mock

        repository_mock = _set_up_mocked_repository()

        rent_request = FilmRentRequest(
            customer_id=700,
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


def test_rent_films_returns_exception_if_one_of_films_not_available():

    def arrangement():
        def _set_up_mocked_repository():
            repository_mock = MagicMock(name="Repository_Instance")
            repository_mock.get_film_by_id = MagicMock(return_value=Film(0, "Matrix 11", "New release"))
            repository_mock.get_customer = MagicMock(resturn_value=Customer(700, rentals=[]))
            repository_mock.reserv_film = MagicMock(side_effect=AvailabilityError('Film not available.'))

            return repository_mock

        repository_mock = _set_up_mocked_repository()

        rent_request = FilmRentRequest(
            customer_id=700,
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