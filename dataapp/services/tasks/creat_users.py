import pprint


from bitrix24.request import Bitrix24
from .. import users


def create_or_update_users():
    bx24 = Bitrix24()
    add_users_to_db(bx24, "user.get")


def add_users_to_db(bx24, method, filter_field={}, id_start=0):
    filter_field[">ID"] = id_start
    params = {
        "filter": filter_field,
        "order": {"ID": "ASC"},
        "start": -1
    }
    data_list = bx24.call(method, params).get("result")
    if data_list and isinstance(data_list, list):
        id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
        users.add_users(data_list)
        add_users_to_db(bx24, method, filter_field, id_start)
