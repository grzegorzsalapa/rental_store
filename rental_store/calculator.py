from rental_store.inventory import Film
from rental_store.client import Client
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

    def calculate_rent_surcharge(self, film: Film, client: Client):

        if film.film_type == "New":
            for item in client.rent_ledger:
                if item["id"] == film.film_id and "date_of_return" not in item.keys():
                    rent_duration = (date.today() - item["date_of_rent"]).days

            return PriceCalculator.premium_price * rent_duration, "SEK"

        elif film.film_type == "Regular":
            return 31, "SEK"

        elif film.film_type == "Old":
            return 21, "SEK"
