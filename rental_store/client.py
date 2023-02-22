class Client:

    def __init__(self, data_storage, client_id=None):
        self.data_storage = data_storage
        if client_id is None:
            self.create()
        else:
            self.client_id = client_id

    @property
    def rent_ledger(self):
        return RentLedger()

    def rents(self, film, up_front_days, charge, date_of_rent):
        pass

    def create(self):
        self.client_id = self.data_storage.create_client_and_set_id()


class RentLedger:
    def __init__(self, film_list):
        self.film_list = film_list
