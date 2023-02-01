import sys
import pprint

sys.setrecursionlimit(3000)

from bitrix24.request import Bitrix24
from .. import deals


def create_or_update_deals(begin_date=None, end_date=None):
    # begin_date - включительно
    # end_date - не включительно
    bx24 = Bitrix24()
    filter_field = {}
    if begin_date:
        filter_field[">DATE_CREATE"] = begin_date
    if begin_date:
        filter_field["<DATE_CREATE"] = end_date

    total = get_total(bx24, "crm.deal.list", filter_field)
    add_deals_to_db(bx24, "crm.deal.list", filter_field, total)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")


def add_deals_to_db(bx24, method, filter_field={}, total=0, count=0, id_start=0):
        filter_field[">ID"] = id_start
        params = {
            "select": ["*", "UF_*"],
            "filter": filter_field,
            "order": {"ID": "ASC"},
            "start": -1
        }
        data_list = bx24.call(method, params).get("result")
        if data_list and isinstance(data_list, list):
            count += 50
            id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
            # pprint.pprint(data_list)
            for data in data_list:
                deals.create_or_update_deal(data, True)

            print(f"Сделки: {min(count, total)} из {total}", end="\r")
            add_deals_to_db(bx24, method, filter_field, total, count, id_start)

