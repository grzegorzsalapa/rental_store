from rental_store.data_interface import Film, Customer, PriceList
from datetime import date, datetime


def calculate_rent_charge(price_list: PriceList, film: Film, up_front_days):

    premium_price = price_list.premium_price
    basic_price = price_list.basic_price
    currency = price_list.currency

    print(premium_price)

    if film.film_type == "New release":
        charge = premium_price * up_front_days

        return charge, currency

    elif film.film_type == "Regular":
        return 30, "SEK"

    elif film.film_type == "Old":
        return 20, "SEK"


def calculate_rent_surcharge(price_list: PriceList, film: Film, customer: Customer):

    premium_price = price_list.premium_price
    basic_price = price_list.basic_price
    currency = price_list.currency

    if film.film_type == "New release":
        for item in customer.rent_ledger:
            if item["film_id"] == film.film_id and "date_of_return" not in item.keys():
                rent_duration = (date.today() - item["date_of_rent"]).days
                overdue = rent_duration - item["up_front_days"]

        charge = overdue * premium_price

        return charge, currency

    elif film.film_type == "Regular":
        return 31, "SEK"

    elif film.film_type == "Old":
        return 21, "SEK"
