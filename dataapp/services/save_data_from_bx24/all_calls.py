import sys
sys.setrecursionlimit(11000)

from .. import save_call


def save_to_db(bx24):
    total_calls = get_total(bx24, "voximplant.statistic.get", {">CALL_START_DATE": "2022-01-01"})
    save_calls_to_db(bx24, total_calls)


def save_calls_to_db(bx24, total=0, count=0, id_start=0):
    params = {
        "select": [
            "ID", "CALL_ID", "CALL_TYPE", "PHONE_NUMBER", "CALL_DURATION",
            "CALL_START_DATE", "CRM_ACTIVITY_ID", "PORTAL_USER_ID"
        ],
        "FILTER": {
            ">ID": id_start,
            ">CALL_START_DATE": "2022-01-01",
            # "<CALL_START_DAeTE": "2022-01-01",
        },
        "SORT": "ID",
        "ORDER": "ASC",
        "start": -1
    }

    calls_list = bx24.call("voximplant.statistic.get", params).get("result")
    if calls_list and isinstance(calls_list, list):
        count += 50
        id_start = calls_list[-1].get("ID")
        for call in calls_list:
            res = save_call.add_call_drf(call)
            if res:
                print("INPUT: ", call)
                print("OUTPUT: ", res)

        print(f"Получено {count} из {total}")
        save_calls_to_db(bx24, total, count, id_start)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")


# def add_calls_to_db(bx24, method, filter_field={}, total=0, count=0, id_start=0):
#         filter_field[">ID"] = id_start
#         params = {
#             "SELECT": ["ID", "CALL_ID", "CALL_TYPE", "PHONE_NUMBER", "CALL_DURATION", "CALL_START_DATE", "CRM_ACTIVITY_ID", "PORTAL_USER_ID"],
#             "FILTER": filter_field,
#             "SORT": "ID",
#             "ORDER": "ASC",
#             "start": -1
#         }
#         data_list = bx24.call(method, params).get("result")
#         if data_list and isinstance(data_list, list):
#             count += 50
#             id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
#             for data in data_list:
#                 calls.create_or_update_call(data)
#
#             print(id_start)
#             print(f"{min(count, total)} из {total}")  # , end="\r")
#             add_calls_to_db(bx24, method, filter_field, total, count, id_start)
#
#
# def create_or_update_calls(begin_date=None, end_date=None):
#     # begin_date - включительно
#     # end_date - не включительно
#     bx24 = Bitrix24()
#     filter_field = {}
#     if begin_date:
#         filter_field[">CALL_START_DATE"] = begin_date
#     if begin_date:
#         filter_field["<CALL_START_DATE"] = end_date
#
#     filter_field[">CALL_START_DATE"] = "2022-01-01"
#
#     total = get_total(bx24, "voximplant.statistic.get", filter_field)
#     add_calls_to_db(bx24, "voximplant.statistic.get", filter_field, total)


