# def _set_up_mocked_data_storage(client_id=None, client_metadata=None):
#
#     data_storage = MagicMock(name="DataStorage_Instance")
#     data_storage.add_client_and_set_id = MagicMock(return_value=client_id)
#     data_storage.get_client = MagicMock(return_value=client_metadata)
#     data_storage.add_client_rented_items = MagicMock()
#     data_storage.add_item_types = MagicMock()
#     data_storage.get_item_types = MagicMock()
#     data_storage.add_items_to_inventory = MagicMock()
#     data_storage.get_all_items_from_inventory = MagicMock()
#     data_storage.get_items_from_inventory = MagicMock()
#
#     return data_storage
