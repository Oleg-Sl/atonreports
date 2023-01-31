import pprint

from bitrix24.request import Bitrix24
from .. import calls

def create_or_update_calls(begin_date=None, end_date=None):
    # begin_date - включительно
    # end_date - не включительно
    bx24 = Bitrix24()
    filter_field = {}
    if begin_date:
        filter_field[">CALL_START_DATE"] = begin_date
    if begin_date:
        filter_field["<CALL_START_DATE"] = end_date

    total = get_total(bx24, "voximplant.statistic.get", filter_field)
    add_calls_to_db(bx24, "voximplant.statistic.get", filter_field, total)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")


def add_calls_to_db(bx24, method, filter_field={}, total=0, count=0, id_start=0):
        filter_field[">ID"] = id_start
        params = {
            "FILTER": filter_field,
            "SORT": "ID",
            "ORDER": "ASC",
            "start": -1
        }
        data_list = bx24.call(method, params).get("result")
        if data_list and isinstance(data_list, list):
            count += 50
            id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
            for data in data_list:
                calls.create_or_update_call(data)

            print(f"{min(count, total)} из {total}", end="\r")
            add_calls_to_db(bx24, method, filter_field, total, count, id_start)
