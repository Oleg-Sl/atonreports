def get_data(bx24, ids):
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


def get_requisite(bx24, ids):
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


def get_address(bx24, ids):
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
