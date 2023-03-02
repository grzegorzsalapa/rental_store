import uuid
from datetime import date, timedelta

from rental_store.models import Film, PriceList
from rental_store.service.calculator import calculate_rent_charge, calculate_rent_surcharge


def test_calculate_rent_charge_for_new_release():
    def arrangement():
        price_list = PriceList(currency="SEK", premium_price=40, basic_price=30)
        film = Film(id=0, title="Matrix 11", type="New release", items_total=50)
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
        price_list = PriceList(currency="SEK", premium_price=40, basic_price=30)
        film = Film(id=0, title="Matrix 11", type="New release", items_total=50)

        request_id = uuid.uuid4()
        up_front_days = 1

        today = date.today()
        d = timedelta(days=3)
        date_of_rent = (today - d)

        return price_list, film, up_front_days, date_of_rent

    def action(price_list, film, up_front_days, date_of_rent):
        charge = calculate_rent_surcharge(price_list, film, up_front_days, date_of_rent)

        return charge

    def assertion(charge):
        assert charge == (80, "SEK")

    price_list, film, up_front_days, date_of_rent = arrangement()
    action_result = action(price_list, film, up_front_days, date_of_rent)
    assertion(action_result)
