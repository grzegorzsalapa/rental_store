from rental_store.inventory import Film


class PriceCalculator:

    def calculate_rent_charge(self, film: Film, up_front_days):
        return 40, "SEK"

    def calculate_rent_surcharge(self, film: Film):
        return 30, "SEK"
