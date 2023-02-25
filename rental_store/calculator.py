from rental_store.data_models import Film, Customer, PriceList
from datetime import date


def calculate_rent_charge(price_list: PriceList, film: Film, up_front_days):

    if film.type == "New release":
        charge = price_list.premium_price * up_front_days

        return charge, price_list.currency

    elif film.type == "Regular":
        return 30, "SEK"

    elif film.type == "Old":
        return 20, "SEK"


def calculate_rent_surcharge(price_list: PriceList, film: Film, customer: Customer):

    if film.type == "New release":
        for record in customer.rentals:
            if record.film_id == film.id and record.date_of_return is None:
                rent_duration = (date.today() - record.date_of_rent).days
                overdue = rent_duration - record.up_front_days

        charge = max(0, overdue) * price_list.premium_price

        return charge, price_list.currency

    elif film.type == "Regular":
        return 31, "SEK"

    elif film.type == "Old":
        return 21, "SEK"
