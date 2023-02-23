from rental_store.repository_interface import RentLedger, Film


class Customer:

    def __init__(self, data_storage, customer_id=None):
        self.data_storage = data_storage
        if customer_id is None:
            self.create()
        else:
            self.customer_id = customer_id

    def create(self):
        self.customer_id = self.data_storage.create_customer_and_set_id()

    @property
    def rent_ledger(self) -> list:
        return self.data_storage.get_customers_rent_ledger(self.customer_id)

    def rents(self, film: Film, up_front_days: int, charge: int, date_of_rent):
        self.data_storage.add_film_to_customers_ledger(self.customer_id, film, up_front_days, charge, date_of_rent)

    def returns(self, film: Film, surcharge, date_of_return):
        self.data_storage.mark_film_as_returned_in_customers_ledger(self.customer_id, film, surcharge, date_of_return)



