import sys
sys.setrecursionlimit(8000)

# from bitrix24.request import Bitrix24
from .. import save_activity


def save_to_db(bx24):
    total_activities = get_total(bx24, "crm.activity.list", {"TYPE_ID": "2",})
    save_activities_to_db(bx24, total_activities)


def save_activities_to_db(bx24, total=0, count=0, id_start=0):
    params = {
        "select": [
            "ID", "COMPLETED", "DIRECTION", "TYPE_ID", "STATUS", "OWNER_TYPE_ID",
            "OWNER_ID", "CREATED", "END_TIME", "RESPONSIBLE_ID"
        ],
        "filter": {
            # "TYPE_ID": "1",
            "TYPE_ID": "2",
            ">ID": id_start,
            ">CREATED": "2022-01-01",
            # "<CREATED": None
        },
        "order": {"ID": "ASC"},
        "start": -1
    }
    activities_list = bx24.call("crm.activity.list", params).get("result")
    if activities_list and isinstance(activities_list, list):
        count += 50
        id_start = activities_list[-1].get("ID")
        activities_company_ = get_companies_for_activities(bx24, activities_list)
        for activity in activities_list:
            activity.update(activities_company_.get(activity.get("ID")))
            res = save_activity.add_activity_drf(activity)
            if res:
                print("INPUT: ", activity)
                print("OUTPUT: ", res)

        print(f"Получено {count} из {total}")
        save_activities_to_db(bx24, total, count, id_start)


def get_companies_for_activities(bx24, activities_data):
    # Формирование списка batch запросов
    result = {}
    cmd = {}
    for activity_data in activities_data:
        activity_id = activity_data.get("ID")
        if activity_data["OWNER_TYPE_ID"] == "1" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.lead.get?id={activity_data['OWNER_ID']}"
        if activity_data["OWNER_TYPE_ID"] == "2" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.deal.get?id={activity_data['OWNER_ID']}"
        if activity_data["OWNER_TYPE_ID"] == "3" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.contact.get?id={activity_data['OWNER_ID']}"
        if activity_data["OWNER_TYPE_ID"] == "4" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.company.get?id={activity_data['OWNER_ID']}"

    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })
    if not response or "result" not in response or "result" not in response["result"] or not isinstance(response["result"]["result"], dict):
        return result

    entity_data_obj = response["result"]["result"]
    for activity_data in activities_data:
        data_ = {}
        activity_id = activity_data.get("ID")
        entity_data = entity_data_obj.get(activity_id, {})
        if activity_data["OWNER_TYPE_ID"] == "1":
            data_["COMPANY_ID"] = entity_data.get("COMPANY_ID")
            data_["OWNER_NAME"] = entity_data.get("TITLE")
        if activity_data["OWNER_TYPE_ID"] == "2":
            data_["COMPANY_ID"] = entity_data.get("COMPANY_ID")
            data_["OWNER_NAME"] = entity_data.get("TITLE")
        if activity_data["OWNER_TYPE_ID"] == "3":
            data_["COMPANY_ID"] = entity_data.get("COMPANY_ID")
            lastname = entity_data.get("LAST_NAME", "")
            name = entity_data.get("NAME", "")
            data_["OWNER_NAME"] = f"{lastname} {name}"
        if activity_data["OWNER_TYPE_ID"] == "4":
            data_["COMPANY_ID"] = entity_data.get("ID")
            data_["OWNER_NAME"] = entity_data.get("TITLE")
        result[activity_id] = data_

    return result


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")


# def creat_and_update_activities(begin_date=None, end_date=None):
#     # begin_date - включительно
#     # end_date - не включительно
#     bx24 = Bitrix24()
#     filter_field = {}
#     if begin_date:
#         filter_field[">CREATED"] = begin_date
#     if begin_date:
#         filter_field["<CREATED"] = end_date
#
#     filter_field[">CREATED"] = "2023-02-01"
#     # filter_field["TYPE_ID"] = "1"
#
#         # "filter": {
#         #     "TYPE_ID": "2",
#         #     ">CREATED": "2022-01-01"
#         # },
#
#     total = get_total(bx24, "crm.activity.list", filter_field)
#     add_activities_to_db(bx24, "crm.activity.list", filter_field, total)
#
#
# def add_activities_to_db(bx24, method, filter_field={}, total=0, count=0, id_start=0):
#         filter_field[">ID"] = id_start
#         params = {
#             "select": ["ID", "COMPLETED", "DIRECTION", "TYPE_ID", "STATUS", "OWNER_TYPE_ID", "OWNER_ID", "CREATED", "END_TIME", "RESPONSIBLE_ID"],
#             "filter": filter_field,
#             "order": {"ID": "ASC"},
#             "start": -1
#         }
#         data_list = bx24.call(method, params).get("result")
#         if data_list and isinstance(data_list, list):
#             count += 50
#             id_start = data_list[-1].get("ID") or data_list[-1].get("ID")
#             companies_obj = get_companies_for_activities(bx24, data_list)
#             for data in data_list:
#                 activity_id_ = data.get("ID")
#                 activities.create_or_update_activity(data, companies_obj.get(activity_id_))
#
#             print(id_start)
#             print(f"{count} из {total}")#, end="\r")
#             # print(f"{min(count, total)} из {total}")#, end="\r")
#             add_activities_to_db(bx24, method, filter_field, total, count, id_start)

