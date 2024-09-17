import sys
sys.setrecursionlimit(11000)

from .. import save_call


def save_to_db(bx24, data):
    total_calls = get_total(bx24, "voximplant.statistic.get", data)
    save_calls_to_db(bx24, data, total_calls)


def save_calls_to_db(bx24, filter_data, total=0, count=0, id_start=0):
    filter_data[">ID"] = id_start
    params = {
        "select": [
            "ID", "CALL_ID", "CALL_TYPE", "PHONE_NUMBER", "CALL_DURATION",
            "CALL_START_DATE", "CRM_ACTIVITY_ID", "PORTAL_USER_ID"
        ],
        "filter": filter_data,
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

        print(f"Получено {count} из {total}")
        save_calls_to_db(bx24, filter_data, total, count, id_start)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")
