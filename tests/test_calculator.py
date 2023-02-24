import pytest
from rental_store.calculator import calculate_rent_charge, calculate_rent_surcharge
from rental_store.data_models import Film, Customer, PriceList
from datetime import date, timedelta


def test_calculate_rent_charge_for_new_release():

    def arrangement():

        price_list = PriceList("SEK", 40, 30)
        film = Film(0, "Matrix 11", "New release")
        up_front_days = 1

        return price_list, film, up_front_days

    def action(price_list, film, up_front_days):
        charge = calculate_rent_charge(price_list, film, up_front_days)

        return charge

    def assertion(charge):
        assert charge == (40, "SEK")

    price_list, film, up_front_days = arrangement()
    action_result = action(price_list, film, up_front_days)
    assertion(action_result)


def test_calculate_rent_surcharge_for_new_release():

    def arrangement():

        price_list = PriceList("SEK", 40, 30)
        film = Film(0, "Matrix 11", "New release")

        today = date.today()
        d = timedelta(days=3)
        rent_date = (today - d)

        print(rent_date)

        rentals = [
            {
                "film_id": 0,
                "up_front_days": 1,
                "charge": 40,
                "date_of_rent": rent_date
            }
        ]

        customer = Customer(7, rentals)

        return price_list, film, customer

    def action(price_list, film, customer):
        charge = calculate_rent_surcharge(price_list, film, customer)

        return charge

    def assertion(charge):
        assert charge == (80, "SEK")

    price_list, film, customer = arrangement()
    action_result = action(price_list, film, customer)
    assertion(action_result)
