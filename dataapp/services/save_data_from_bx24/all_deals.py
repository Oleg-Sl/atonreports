import sys
import time
sys.setrecursionlimit(3000)

from .. import save_deal


def save_to_db(bx24, data):
    total_deals = get_total(bx24, "crm.deal.list", data)
    print(total_deals)
    save_deals_to_db(bx24, data, total_deals)


def save_deals_to_db(bx24, filter_data, total=0, count=0, id_start=0):
    print("===")
    filter_data[">ID"] = id_start
    params = {
        "select": [
            "CATEGORY_ID", "UF_CRM_1610523951", "TITLE", "ID", "DATE_CREATE", "DATE_MODIFY", "CLOSEDATE",
            "CLOSED", "OPPORTUNITY", "UF_CRM_1575629957086", "UF_CRM_1575375338", "COMPANY_ID", "STAGE_ID"
        ],
        "filter": filter_data,
        "order": {"ID": "ASC"},
        "start": -1
    }

    print(params)
    deals_list = bx24.call("crm.deal.list", params).get("result")
    print(deals_list)

    if deals_list and isinstance(deals_list, list):
        count += 50
        id_start = deals_list[-1].get("ID")
        for deal in deals_list:
            deal['active'] = True
            res = save_deal.add_deal_drf(deal)

        print(f"Получено {count} из {total}")
        time.sleep(0.4)
        save_deals_to_db(bx24, filter_data, total, count, id_start)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    print(response)
    return response.get("total")
