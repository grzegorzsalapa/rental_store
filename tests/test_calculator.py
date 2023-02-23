import pytest
from unittest.mock import patch, MagicMock
from rental_store.calculator import PriceCalculator
from rental_store.repository_interface import Film
from rental_store.customer import Customer
from datetime import date, timedelta


def test_calculate_rent_charge_for_new_release():

    def arrangement():
        up_front_days = 1
        film_mock = Film(0, "Matrix 11", "New release")

        return film_mock, up_front_days

    def action(film_mock, up_front_days):

        price_calculator = PriceCalculator()
        charge = price_calculator.calculate_rent_charge(film_mock, up_front_days)

        return charge

    def assertion(charge):
        assert charge == (40, "SEK")

    film_mock, up_front_days = arrangement()
    action_result = action(film_mock, up_front_days)
    assertion(action_result)


def test_calculate_rent_surcharge_for_new_release():

    def arrangement():

        film_mock = Film(0, "Matrix 11", "New release")

        class CustomerMock(MagicMock):

            def rent_ledger(self):

                today = date.today()
                d = timedelta(days=3)
                rent_date = (today - d).day

                rent_ledger_mock = [
                    {
                        "film_id": 0,
                        "up_front_days": 1,
                        "charge": 40,
                        "date_of_rent": rent_date
                    }
                ]

                return rent_ledger_mock

        return film_mock, CustomerMock

    def action(film_mock):

        data_storage = MagicMock()
        test_customer = Customer(data_storage)
        price_calculator = PriceCalculator()

        charge = price_calculator.calculate_rent_charge(film_mock, test_customer)

        return charge

    def assertion(charge):
        assert charge == (40, "SEK")

    film_mock, CustomerMock = arrangement()

    with patch('tests.test_calculator.Customer', new=CustomerMock):
        action_result = action(film_mock)
        assertion(action_result)
