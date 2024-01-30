import sys
sys.setrecursionlimit(3000)

from .. import save_deal


def save_to_db(bx24, data):
    # total_deals = get_total(bx24, "crm.deal.list", {">DATE_CREATE": "2023-04-15"})
    total_deals = get_total(bx24, "crm.deal.list", data)
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
        # "filter": {
        #     ">ID": id_start,
        #     ">DATE_CREATE": "2023-04-15",
        #     # "<DATE_CREATE": None
        # },
        "order": {"ID": "ASC"},
        "start": -1
    }

    deals_list = bx24.call("crm.deal.list", params).get("result")

    if deals_list and isinstance(deals_list, list):
        count += 50
        id_start = deals_list[-1].get("ID")
        for deal in deals_list:
            deal['active'] = True
            res = save_deal.add_deal_drf(deal)
            # if res:
                # print("INPUT: ", deal)
                # print("INPUT: ", deal.get("ID"))
                # print("OUTPUT=> ", res)

        print(f"Получено {count} из {total}")
        save_deals_to_db(bx24, filter_data, total, count, id_start)


# def create_or_update_deals(begin_date=None, end_date=None):
#     # begin_date - включительно
#     # end_date - не включительно
#     bx24 = Bitrix24()
#     filter_field = {}
#     if begin_date:
#         filter_field[">DATE_CREATE"] = begin_date
#     if begin_date:
#         filter_field["<DATE_CREATE"] = end_date
#
#     total = get_total(bx24, "crm.deal.list", filter_field)
#     add_deals_to_db(bx24, "crm.deal.list", filter_field, total)
#
#
# def add_deals_to_db(bx24, method, filter_field={}, total=0, count=0, id_start=0):
#         filter_field[">ID"] = id_start
#         params = {
#             "select": ["CATEGORY_ID", "UF_CRM_1610523951", "TITLE", "ID", "DATE_CREATE", "DATE_MODIFY", "CLOSEDATE", "CLOSED", "OPPORTUNITY", "UF_CRM_1575629957086", "UF_CRM_1575375338", "COMPANY_ID", "STAGE_ID"],
#             "filter": filter_field,
#             "order": {"ID": "ASC"},
#             "start": -1
#         }
#         data_list = bx24.call(method, params).get("result")
#         if data_list and isinstance(data_list, list):
#             count += 50
#             id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
#             # pprint.pprint(data_list)
#             for data in data_list:
#                 deals.create_or_update_deal(data, True)
#             print(id_start)
#             print(f"Сделки: {min(count, total)} из {total}") #, end="\r")
#             add_deals_to_db(bx24, method, filter_field, total, count, id_start)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")

