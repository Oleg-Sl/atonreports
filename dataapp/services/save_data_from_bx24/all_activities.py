import sys
sys.setrecursionlimit(8000)

from .. import save_activity


def save_to_db(bx24, data):
    data["TYPE_ID"] = "2"
    total_activities = get_total(bx24, "crm.activity.list", data)
    save_activities_to_db(bx24, data, total_activities)


def save_activities_to_db(bx24, filter_data, total=0, count=0, id_start=0):
    filter_data[">ID"] = id_start
    params = {
        "select": [
            "ID", "COMPLETED", "DIRECTION", "TYPE_ID", "STATUS", "OWNER_TYPE_ID",
            "OWNER_ID", "CREATED", "END_TIME", "RESPONSIBLE_ID"
        ],
        "filter": filter_data,
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
        print(f"Получено {count} из {total}")
        save_activities_to_db(bx24, filter_data, total, count, id_start)


def get_companies_for_activities(bx24, activities_data):
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
        "filter": filter_field,
    }
    response = bx24.call(method, params)
    print(response)
    return response.get("total")
