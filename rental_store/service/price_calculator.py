from datetime import date

from rental_store.models import Film, PriceList


class PriceCalculator:

    def __init__(self, price_list: PriceList, regular_flat_days: int, old_flat_days: int):
        self.price_list = price_list
        self.regular_flat_days = regular_flat_days
        self.old_flat_days = old_flat_days

    def calculate_rent_charge(self, film: Film, up_front_days: int):
        if film.type == "New release":

            charge = self.price_list.premium_price * up_front_days

            return charge, self.price_list.currency

        elif film.type == "Regular":

            charge = max(self.regular_flat_days, up_front_days) * self.price_list.basic_price

            return charge, self.price_list.currency

        elif film.type == "Old":

            charge = max(self.old_flat_days, up_front_days) * self.price_list.basic_price

            return charge, self.price_list.currency

    def calculate_rent_surcharge(self, film: Film, up_front_days: int, date_of_rent: date):
        if film.type == "New release":

            rent_duration = (date.today() - date_of_rent).days
            overdue = max(0, rent_duration - up_front_days)

            charge = overdue * self.price_list.premium_price

            return charge, self.price_list.currency

        elif film.type == "Regular":

            rent_duration = (date.today() - date_of_rent).days
            overdue = max(0, rent_duration - max(self.regular_flat_days, up_front_days))

            charge = overdue * self.price_list.basic_price

            return charge, self.price_list.currency

        elif film.type == "Old":

            rent_duration = (date.today() - date_of_rent).days
            overdue = max(0, rent_duration - max(self.old_flat_days, up_front_days))

            charge = overdue * self.price_list.basic_price

            return charge, self.price_list.currency
