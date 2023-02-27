from rental_store.data_models import Film, Customer, PriceList
from datetime import date


def calculate_rent_charge(price_list: PriceList, film: Film, up_front_days: date):

    if film.type == "New release":
        charge = price_list.premium_price * up_front_days

        return charge, price_list.currency

    elif film.type == "Regular":
        return 30, "SEK"

    elif film.type == "Old":
        return 20, "SEK"


def calculate_rent_surcharge(price_list: PriceList, film: Film, up_front_days: int, date_of_rent: date):

    if film.type == "New release":

        rent_duration = (date.today() - date_of_rent).days
        overdue = max(0, rent_duration - up_front_days)

        charge = overdue * price_list.premium_price

        return charge, price_list.currency

    elif film.type == "Regular":
        return 31, "SEK"

    elif film.type == "Old":
        return 21, "SEK"
