import pprint

from . import utils
from dataapp.models import Activity, Stage, Deal, Direction, User, Company


def get_data_activities(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"crm.activity.get?id={id_}"

    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })
    # pprint.pprint(response)
    if not response or "result" not in response or "result" not in response["result"]:
        return

    return response["result"]["result"]


def create_or_update_activity(activity_data, companies_data, active=True):
    data = {
        "COMPLETED": activity_data.get("COMPLETED", None),
        "DIRECTION": activity_data.get("DIRECTION", None),
        "TYPE_ID": activity_data.get("TYPE_ID", None),
        "STATUS": activity_data.get("STATUS", None),
        "OWNER_TYPE_ID": activity_data.get("OWNER_TYPE_ID", None),
        "OWNER_ID": activity_data.get("OWNER_ID", None),
        "CREATED": activity_data.get("CREATED", None) or None,
        "END_TIME": activity_data.get("END_TIME", None) or None,
        "OWNER_NAME": companies_data.get("OWNER_NAME", None),
        "active": active,
        # из связанных таблиц
        "RESPONSIBLE_ID": User.objects.filter(ID=activity_data.get("RESPONSIBLE_ID")).first(),
        "COMPANY_ID": Company.objects.filter(ID=companies_data.get("COMPANY_ID")).first(),
        # из сущности звонка
        # "DURATION": duration,
        # "CALL_START_DATE": call_start_date,
    }

    obj_, created = Activity.objects.update_or_create(
        ID=activity_data.get("ID", None),
        defaults=data
    )
    return obj_


def change_activity_active(activity_id, active):
    activity_obj = Activity.objects.filter(ID=activity_id).update(active=active)
    return activity_obj


def get_companies_for_activities(bx24, activities_data):
    # Формирование списка batch запросов
    cmd = {}
    for activity_id, activity_data in activities_data.items():
        # pprint.pprint(activity_data)
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
