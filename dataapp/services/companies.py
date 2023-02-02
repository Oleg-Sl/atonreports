import pprint

from dataapp.models import Activity, Stage, Deal, Direction, User, Company


def get_company_data(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"crm.company.get?id={id_}"

    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })

    if not response or "result" not in response or "result" not in response["result"]:
        return

    return response["result"]["result"]


def get_company_requisite(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"crm.requisite.list?filter[ENTITY_ID]={id_}&filter[ENTITY_TYPE_ID]=4&select[]=RQ_INN"

    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })

    if not response or "result" not in response or "result" not in response["result"]:
        return

    result = {}
    for company_id, req_ in response["result"]["result"].items():
        result[company_id] = req_[0].get("RQ_INN", None) if req_ else None

    return result


def get_company_requisite_address(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"crm.address.list?filter[ENTITY_ID]={id_}&filter[ENTITY_TYPE_ID]=4&select[]=ENTITY_ID&select[]=REGION&select[]=CITY&select[]=PROVINCE"

    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })

    if not response or "result" not in response or "result" not in response["result"]:
        return

    result = {}
    for company_id, addr_ in response["result"]["result"].items():
        result[company_id] = addr_[0] if addr_ else {}

    return result


def create_or_update_company(company_data, inn=None, address={}, active=True):
    """ Сохранение компании из BX24 """
    data = {}
    data["ASSIGNED_BY_ID"] = User.objects.filter(ID=company_data.get("ASSIGNED_BY_ID")).first()
    data["TITLE"]=company_data.get("TITLE")
    data["DATE_CREATE"]=company_data.get("DATE_CREATE")
    data["ADDRESS"]=company_data.get("ADDRESS")
    data["REVENUE"]=company_data.get("REVENUE")
    data["INDUSTRY"]=company_data.get("INDUSTRY")
    data["sector"]=company_data.get("UF_CRM_1640828035")
    data["region"]=company_data.get("UF_CRM_1639121988")
    data["source"]=company_data.get("UF_CRM_1639121612")
    data["number_employees"]=company_data.get("UF_CRM_1639121303")
    data["district"]=company_data.get("UF_CRM_1639121341")
    data["main_activity"]=company_data.get("UF_CRM_1617767435")
    data["other_activities"]=company_data.get("UF_CRM_1639121225")
    data["profit"]=company_data.get("UF_CRM_1639121262")
    data["requisite_region"] = address.get("REGION")
    data["requisites_city"] = address.get("CITY")
    data["requisites_province"] = address.get("PROVINCE")
    data["inn"] = inn
    data["active"] = active

    company_obj = Company.objects.update_or_create(ID=company_data.get("ID"), defaults=data)
    return company_obj


def create_or_update_requisite(requisite_data):
    """ Сохранение ИНН компании из BX24 """
    company_obj = Company.objects.filter(ID=requisite_data.get("ENTITY_ID")).update(inn=requisite_data.get("RQ_INN"))
    return company_obj


def create_or_update_address(address_data):
    """ Сохранение адреса компании из BX24 """
    company_obj = Company.objects.filter(ID=address_data.get("ENTITY_ID")).update(
        requisite_region=address_data.get("REGION"),
        requisites_city=address_data.get("CITY"),
        requisites_province=address_data.get("PROVINCE"),
    )
    return company_obj


def change_company_active(company_id, active):
    """ Сохранение компании из BX24 """
    company_obj = Company.objects.filter(ID=company_id).update(active=active)
    return company_obj

