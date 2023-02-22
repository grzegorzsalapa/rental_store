from rental_store.inventory import Film
from rental_store.client import Client


class PriceCalculator:

    def calculate_rent_charge(self, film: Film, up_front_days):
        return 40, "SEK"

    def calculate_rent_surcharge(self, film: Film, client: Client):
        return 30, "SEK"
