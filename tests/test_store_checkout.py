import pytest
from unittest.mock import MagicMock, patch
from rental_store.data_models import \
    FilmRentRequestModel,\
    FilmRentRequestItemModel,\
    FilmRentResponseModel,\
    FilmRentResponseItemModel,\
    Film,\
    Customer
from rental_store.store_checkout import AvailabilityError, rent_films, return_films


def test_rent_films_assignes_film_to_customer_in_rental_ledger():

    def arrangement():

        film_id = 14
        film = Film(film_id, "Matrix 11", "New release", 265)

        def _set_up_mocked_repository():
            RepositoryMock = MagicMock(name="Repository_Instance")
            RepositoryMock.get_film_by_id.return_value = film
            RepositoryMock.get_customer = MagicMock(resturn_value=Customer(customer_id=700, rentals=[]))
            RepositoryMock.reserve_film = MagicMock()
            RepositoryMock.add_record_to_rental_ledger = MagicMock()

            return RepositoryMock

        RepositoryMock = _set_up_mocked_repository()

        rent_request = FilmRentRequestModel(
            customer_id=700,
            rented_films=[
                FilmRentRequestItemModel(
                    film_id=film_id,
                    up_front_days=8
                )
            ]
        )

        return RepositoryMock, rent_request, film

    def action(rent_request):

        result = rent_films(rent_request)

        return result

    def assertion(result, calculate_rent_charge_mock, film, RepositoryMock):

        film_rent_response = FilmRentResponseModel(
            rented_films=[
                FilmRentResponseItemModel(
                    film_id=14,
                    charge=40,
                    currency="SEK"
                )
            ]
        )

        assert result == film_rent_response
        assert RepositoryMock.get_customer.assert_called_once_with(700)
        assert calculate_rent_charge_mock.assert_called_once_with(film, 8)


    RepositoryMock, rent_request, film = arrangement()
    with patch('rental_store.store_checkout.Repository', new=RepositoryMock):
        with patch('rental_store.store_checkout.calculate_rent_charge', return_value=(40, "SEK"))\
                as calculate_rent_charge_mock:
            result = action(rent_request)
            assertion(result, calculate_rent_charge_mock, film, RepositoryMock)


# def test_rent_films_returns_exception_if_one_of_films_not_available():
#
#     def arrangement():
#         def _set_up_mocked_repository():
#             RepositoryMock = MagicMock(name="Repository_Instance")
#             RepositoryMock.get_film_by_id = MagicMock(return_value=Film(0, "Matrix 11", "New release"))
#             RepositoryMock.get_customer = MagicMock(resturn_value=Customer(700, rentals=[]))
#             RepositoryMock.reserve_film = MagicMock()
#
#             return RepositoryMock
#
#         RepositoryMock = _set_up_mocked_repository()
#
#         rent_request = FilmRentRequestModel(
#             customer_id=700,
#             rented_films=[
#                 FilmRentRequestItemModel(
#                     film_id=0,
#                     up_front_days=1
#                 )
#             ]
#         )
#
#         return RepositoryMock, rent_request
#
#     def action(rent_request):
#
#         result = rent_films(rent_request)
#
#         return result
#
#     def assertion(result):
#
#         film_rent_response = FilmRentResponseModel(
#             rented_films=[
#                 FilmRentResponseItemModel(
#                     film_id=0,
#                     charge=40,
#                     currency="SEK"
#                 )
#             ]
#         )
#
#         assert result == film_rent_response
#
#     RepositoryMock, rent_request = arrangement()
#     with patch('rental_store.store_checkout.Repository', new=RepositoryMock):
#         with patch('rental_store.store_checkout.calculate_rent_charge', return_value=(40, "SEK")):
#             result = action(rent_request)
#             assertion(result)