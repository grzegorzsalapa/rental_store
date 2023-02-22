from rental_store.inventory import Film


class Client:

    def __init__(self, data_storage, client_id=None):
        self.data_storage = data_storage
        if client_id is None:
            self.create()
        else:
            self.client_id = client_id

    def create(self):
        self.client_id = self.data_storage.create_client_and_set_id()

    @property
    def rent_ledger(self):
        return RentLedger()

    def rents(self, film: Film, up_front_days: int, charge: int, date_of_rent):
        self.data_storage.add_film_to_clients_ledger(film.film_id, up_front_days, charge, date_of_rent)

    def returns(self, film: Film, surcharge, date_of_return):
        self.data_storage.mark_film_as_returned_in_clients_ledger(film.film_id, surcharge, date_of_return)


class RentLedger:
    pass
