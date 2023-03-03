from datetime import date, timedelta

from rental_store.models import Film, PriceList
from rental_store.service.price_calculator import PriceCalculatorImpl

calculator = PriceCalculatorImpl(PriceList(currency="SEK", premium_price=40, basic_price=30), 3, 5)


def test_calculate_rent_charge_for_new_release():
    # given
    def arrangement():
        film = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        up_front_days = 1

        return film, up_front_days

    # when
    def action(film, up_front_days):
        charge = calculator.calculate_rent_charge(film, up_front_days)

        return charge

    # then
    def assertion(charge):
        assert charge == (40, "SEK")

    film, up_front_days = arrangement()
    action_result = action(film, up_front_days)
    assertion(action_result)


def test_calculate_rent_surcharge_for_new_release():
    def arrangement():
        film = Film(id=0, title="Matrix 11", type="New release", items_total=50)
        up_front_days = 1

        today = date.today()
        d = timedelta(days=3)
        date_of_rent = (today - d)

        return film, up_front_days, date_of_rent

    def action(film, up_front_days, date_of_rent):
        charge = calculator.calculate_rent_surcharge(film, up_front_days, date_of_rent)

        return charge

    def assertion(charge):
        assert charge == (80, "SEK")

    film, up_front_days, date_of_rent = arrangement()
    action_result = action(film, up_front_days, date_of_rent)
    assertion(action_result)
