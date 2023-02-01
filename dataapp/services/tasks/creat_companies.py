import sys
import pprint

sys.setrecursionlimit(2000)

from bitrix24.request import Bitrix24
from .. import companies


def create_or_update_companies(begin_date=None, end_date=None):
    # begin_date - включительно
    # end_date - не включительно
    bx24 = Bitrix24()
    filter_field = {}
    if begin_date:
        filter_field[">DATE_CREATE"] = begin_date
    if begin_date:
        filter_field["<DATE_CREATE"] = end_date

    total = get_total(bx24, "crm.company.list", filter_field)
    add_companies_to_db(bx24, "crm.company.list", filter_field, [], total)

    total = get_total(bx24, "crm.requisite.list", {"ENTITY_TYPE_ID": 4, })
    add_requisites_to_db(bx24, "crm.requisite.list", {"ENTITY_TYPE_ID": 4, }, ["ID", "RQ_INN", "ENTITY_ID", ], total)

    total = get_total(bx24, "crm.address.list", {"ENTITY_TYPE_ID": 4, })
    add_address_to_db(bx24, "crm.address.list", {"ENTITY_TYPE_ID": 4, }, ["LOC_ADDR_ID", "REGION", "CITY", "PROVINCE", "ENTITY_ID", ], total)


def add_companies_to_db(bx24, method, filter_field={}, select=[], total=0, count=0, id_start=0):
        filter_field[">ID"] = id_start
        params = {
            "select": select,
            "filter": filter_field,
            "order": {"ID": "ASC"},
            "start": -1
        }
        data_list = bx24.call(method, params).get("result")
        if data_list and isinstance(data_list, list):
            count += 50
            id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
            for data in data_list:
                companies.create_or_update_company(data)

            print(f"Данные компаний: {min(count, total)} из {total}", end="\r")
            add_companies_to_db(bx24, method, filter_field, select, total, count, id_start)


def add_requisites_to_db(bx24, method, filter_field={}, select=[], total=0, count=0, id_start=0):
        filter_field[">ID"] = id_start
        params = {
            "select": select,
            "filter": filter_field,
            "order": {"ID": "ASC"},
            "start": -1
        }
        data_list = bx24.call(method, params).get("result")
        if data_list and isinstance(data_list, list):
            count += 50
            id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
            for data in data_list:
                companies.create_or_update_requisite(data)

            print(f"ИНН компаний: {min(count, total)} из {total}", end="\r")
            add_requisites_to_db(bx24, method, filter_field, select, total, count, id_start)


def add_address_to_db(bx24, method, filter_field={}, select=[], total=0, count=0, id_start=0):
        filter_field[">LOC_ADDR_ID"] = id_start
        params = {
            "select": select,
            "filter": filter_field,
            "order": {"LOC_ADDR_ID": "ASC"},
            "start": -1
        }
        data_list = bx24.call(method, params).get("result")
        if data_list and isinstance(data_list, list):
            count += 50
            id_start = data_list[-1].get("LOC_ADDR_ID") or data_list[-1].get("LOC_ADDR_ID")
            for data in data_list:
                companies.create_or_update_address(data)

            print(f"Адрес компаний: {min(count, total)} из {total}", end="\r")
            add_address_to_db(bx24, method, filter_field, select, total, count, id_start)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")
