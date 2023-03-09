from rental_store.data_models import FilmType, PriceList
from datetime import date


class PriceCalculator:

    def __init__(self, price_list: PriceList, regular_flat_days=3, old_flat_days=5):
        self.price_list = price_list
        self.regular_flat_days = regular_flat_days
        self.old_flat_days = old_flat_days

    def calculate_rent_charge(self, film_type: FilmType, up_front_days: int):

        if film_type == FilmType.NEW_RELEASE:

            charge = self.price_list.premium_price * up_front_days

            return charge

        elif film_type == FilmType.REGULAR:

            charge = max(self.regular_flat_days, up_front_days) * self.price_list.basic_price

            return charge

        elif film_type == FilmType.OLD:

            charge = max(self.old_flat_days, up_front_days) * self.price_list.basic_price

            return charge

    def calculate_rent_surcharge(self, film_type: FilmType, up_front_days: int, date_of_rent: date):

        if film_type == FilmType.NEW_RELEASE:

            rent_duration = (date.today() - date_of_rent).days
            overdue = max(0, rent_duration - up_front_days)

            charge = overdue * self.price_list.premium_price

            return charge

        elif film_type == FilmType.REGULAR:

            rent_duration = (date.today() - date_of_rent).days
            overdue = max(0, rent_duration - max(self.regular_flat_days, up_front_days))

            charge = overdue * self.price_list.basic_price

            return charge

        elif film_type == FilmType.OLD:

            rent_duration = (date.today() - date_of_rent).days
            overdue = max(0, rent_duration - max(self.old_flat_days, up_front_days))

            charge = overdue * self.price_list.basic_price

            return charge
