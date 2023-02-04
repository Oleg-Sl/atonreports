
def get_data_activities(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"crm.activity.get?id={id_}"
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })
    if not response or "result" not in response or "result" not in response["result"]:
        return
    return response["result"]["result"]


def get_companies_for_activities(bx24, activities_data):
    cmd = {}
    for activity_id, activity_data in activities_data.items():
        if activity_data["OWNER_TYPE_ID"] == "1" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.lead.get?id={activity_data['OWNER_ID']}"
        if activity_data["OWNER_TYPE_ID"] == "2" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.deal.get?id={activity_data['OWNER_ID']}"
        if activity_data["OWNER_TYPE_ID"] == "3" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.contact.get?id={activity_data['OWNER_ID']}"
        if activity_data["OWNER_TYPE_ID"] == "4" and activity_data["OWNER_ID"]:
            cmd[activity_id] = f"crm.company.get?id={activity_data['OWNER_ID']}"

    # выполнение запроса к Битрикс24 для получения связанной компании
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })

    if not response or "result" not in response or "result" not in response["result"] or not isinstance(response["result"]["result"], dict):
        return

    # извлечение ID компании и названия сущности
    result = {}
    for activity_id, entity_data  in response["result"]["result"].items():
        data_ = {}
        if activities_data[activity_id]["OWNER_TYPE_ID"] == "1":
            data_["COMPANY_ID"] = entity_data.get("COMPANY_ID")
            data_["OWNER_NAME"] = entity_data.get("TITLE")
        if activities_data[activity_id]["OWNER_TYPE_ID"] == "2":
            data_["COMPANY_ID"] = entity_data.get("COMPANY_ID")
            data_["OWNER_NAME"] = entity_data.get("TITLE")
        if activities_data[activity_id]["OWNER_TYPE_ID"] == "3":
            data_["COMPANY_ID"] = entity_data.get("COMPANY_ID")
            lastname = entity_data.get("LAST_NAME", "")
            name = entity_data.get("NAME", "")
            data_["OWNER_NAME"] = f"{lastname} {name}"
        if activities_data[activity_id]["OWNER_TYPE_ID"] == "4":
            data_["COMPANY_ID"] = entity_data.get("ID")
            data_["OWNER_NAME"] = entity_data.get("TITLE")
        result[activity_id] = data_

    return result
