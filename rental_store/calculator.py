from rental_store.data_models import Film, PriceList
from datetime import date

regular_flat_days = 3
old_flat_days = 5

def calculate_rent_charge(price_list: PriceList, film: Film, up_front_days: int):

    if film.type == "New release":

        charge = price_list.premium_price * up_front_days

        return charge, price_list.currency

    elif film.type == "Regular":

        charge = max(regular_flat_days, up_front_days) * price_list.basic_price

        return charge, price_list.currency

    elif film.type == "Old":

        charge = max(old_flat_days, up_front_days) * price_list.basic_price

        return charge, price_list.currency


def calculate_rent_surcharge(price_list: PriceList, film: Film, up_front_days: int, date_of_rent: date):

    if film.type == "New release":

        rent_duration = (date.today() - date_of_rent).days
        overdue = max(0, rent_duration - up_front_days)

        charge = overdue * price_list.premium_price

        return charge, price_list.currency

    elif film.type == "Regular":

        rent_duration = (date.today() - date_of_rent).days
        overdue = max(0, rent_duration - max(regular_flat_days, up_front_days))

        charge = overdue * price_list.basic_price

        return charge, price_list.currency

    elif film.type == "Old":

        rent_duration = (date.today() - date_of_rent).days
        overdue = max(0, rent_duration - max(old_flat_days, up_front_days))

        charge = overdue * price_list.basic_price

        return charge, price_list.currency
