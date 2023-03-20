import sys
sys.setrecursionlimit(10000)
import datetime

from .. import save_company


def save_to_db(bx24, date_from=datetime.datetime.now() - datetime.timedelta(365), date_to=datetime.datetime.now() + datetime.timedelta(1)):
    filter_data = {
        ">DATE_CREATE": date_from.strftime("%Y-%m-%d"),
        "<DATE_CREATE": date_to.strftime("%Y-%m-%d")
    }
    total_companies = get_total(bx24, "crm.company.list", filter_data)
    save_companies_to_db(bx24, filter_data, total_companies)

    filter_data["ENTITY_TYPE_ID"] = 4
    total_requisites = get_total(bx24, "crm.requisite.list", filter_data)
    save_requisites_to_db(bx24, filter_data, total_requisites)

    total_addresses = get_total(bx24, "crm.address.list", filter_data)
    save_addresses_to_db(bx24, filter_data, total_addresses)


def save_companies_to_db(bx24, filter_data, total=0, count=0, id_start=0):
    filter_data[">ID"] = id_start
    params = {
        "select": [
            "ID", "ASSIGNED_BY_ID", "TITLE", "DATE_CREATE", "ADDRESS", "REVENUE", "INDUSTRY", "UF_CRM_1640828035",
            "UF_CRM_1639121988","UF_CRM_1639121612", "UF_CRM_1639121303", "UF_CRM_1639121341", "UF_CRM_1617767435",
            "UF_CRM_1639121225", "UF_CRM_1639121262"
        ],
        "filter": filter_data,
            # {
            # ">ID": id_start,
            # ">DATE_CREATE": "2022-01-01",
            # "<DATE_CREATE": None
        # },
        "order": {"ID": "ASC"},
        "start": -1
    }

    companies_list = bx24.call("crm.company.list", params).get("result")

    if companies_list and isinstance(companies_list, list):
        count += 50
        id_start = companies_list[-1].get("ID")
        for company in companies_list:
            print("INPUT: ", company.get("ID"))
            res = save_company.add_company_drf(company)
            print("OUTPUT: ", res)

        print(f"Получено {count} из {total}")
        save_companies_to_db(bx24, filter_data, total, count, id_start)


def save_requisites_to_db(bx24, filter_data, total=0, count=0, id_start=0):
    filter_data[">ID"] = id_start
    params = {
        "select": ["ID", "RQ_INN", "ENTITY_ID", ],
        "filter": filter_data,
        #     {
        #     "ENTITY_TYPE_ID": 4,
        #     ">ID": id_start
        # },
        "order": {"ID": "ASC"},
        "start": -1
    }
    requisites_list = bx24.call("crm.requisite.list", params).get("result")
    if requisites_list and isinstance(requisites_list, list):
        count += 50
        id_start = requisites_list[-1].get("ID")
        for requisite in requisites_list:
            print("INPUT: ", requisite.get("ID"))
            requisite["ID"] = requisite.get("ENTITY_ID")
            res = save_company.update_company_drf(requisite)
            print("OUTPUT: ", res)

        print(f"Получено реквизитов {count} из {total}")
        save_requisites_to_db(bx24, filter_data, total, count, id_start)


def save_addresses_to_db(bx24, filter_data, total=0, count=0, id_start=0):
    filter_data[">LOC_ADDR_ID"] = id_start
    params = {
        "select": ["LOC_ADDR_ID", "REGION", "CITY", "PROVINCE", "ENTITY_ID", ],
        "filter": filter_data,
        # "filter": {"ENTITY_TYPE_ID": 4, ">LOC_ADDR_ID": id_start},
        "order": {"LOC_ADDR_ID": "ASC"},
        "start": -1
    }
    addresses_list = bx24.call("crm.address.list", params).get("result")
    if addresses_list and isinstance(addresses_list, list):
        count += 50
        id_start = addresses_list[-1].get("LOC_ADDR_ID")
        for address in addresses_list:
            print("INPUT: ", address.get("LOC_ADDR_ID"))
            address["ID"] = address.get("ENTITY_ID")
            res = save_company.update_company_drf(address)
            print("OUTPUT: ", res)
        print(f"Получено адресов {count} из {total}")
        save_addresses_to_db(bx24, filter_data, total, count, id_start)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")
