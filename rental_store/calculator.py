from rental_store.data_interface import Film, Customer
from datetime import date


class PriceCalculator:

    premium_price = 40
    basic_price = 30

    def calculate_rent_charge(self, film: Film, up_front_days):

        if film.film_type == "New release":
            return PriceCalculator.premium_price * up_front_days, "SEK"

        elif film.film_type == "Regular":
            return 30, "SEK"

        elif film.film_type == "Old":
            return 20, "SEK"

    def calculate_rent_surcharge(self, film: Film, customer: Customer):

        if film.film_type == "New":
            for item in customer.rent_ledger:
                if item["id"] == film.film_id and "date_of_return" not in item.keys():
                    rent_duration = (date.today() - item["date_of_rent"]).days

            return PriceCalculator.premium_price * rent_duration, "SEK"

        elif film.film_type == "Regular":
            return 31, "SEK"

        elif film.film_type == "Old":
            return 21, "SEK"
