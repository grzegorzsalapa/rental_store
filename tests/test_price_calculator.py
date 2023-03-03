import unittest
from datetime import date, timedelta
from rental_store.models import PriceList, FilmType
from rental_store.service.price_calculator import PriceCalculatorImpl


class PriceCalculatorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = PriceCalculatorImpl(PriceList(currency="SEK", premium_price=40, basic_price=30), 3, 5)

    def test_calculate_rent_charge_for_new_release(self):
        # given
        film_type = FilmType.NEW_RELEASE
        up_front_days = 1

        # when
        charge = self.calculator.calculate_rent_charge(film_type, up_front_days)

        # then
        assert charge == (40, "SEK")

    def test_calculate_rent_surcharge_for_new_release(self):
        # given
        film_type = FilmType.NEW_RELEASE
        up_front_days = 1

        today = date.today()
        d = timedelta(days=3)
        date_of_rent = (today - d)

        # when
        charge = self.calculator.calculate_rent_surcharge(film_type, up_front_days, date_of_rent)

        # then
        assert charge == (80, "SEK")
