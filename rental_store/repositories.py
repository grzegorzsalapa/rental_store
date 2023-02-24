import rental_store.config

data_storage = rental_store.config.data_storage_class()


class Repository:

    @classmethod
    def get_customer(cls, customer_id: int):
        pass
