import pprint

from . import utils
from dataapp.models import Stage, Deal, Direction, Company


def get_data(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"crm.deal.get?id={id_}"
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })
    if not response or "result" not in response or "result" not in response["result"]:
        return

    return response["result"]["result"]


def create_or_update_deal(data, active):
    direction = data["CATEGORY_ID"]
    if direction in [43, "43"]:
        direction = data.get("UF_CRM_1610523951", None)

    deal = {
        "ID": data.get("ID"),
        "TITLE": data.get("TITLE"),
        "DATE_CREATE": data.get("DATE_CREATE") or None,
        "DATE_MODIFY": data.get("DATE_MODIFY") or None,
        "CLOSEDATE": data.get("CLOSEDATE") or None,
        "CLOSED": True if data.get("CLOSED") == "Y" else False,
        "opportunity": data.get("OPPORTUNITY"),
        "balance_on_payments": utils.editing_money_in_number(data.get("UF_CRM_1575629957086", "")),
        "amount_paid": utils.editing_money_in_number(data.get("UF_CRM_1575375338", "")),
        "company": Company.objects.filter(ID=data.get("COMPANY_ID")).first(),
        "direction": Direction.objects.filter(ID=direction).first(),
        "stage": Stage.objects.filter(STATUS_ID=data.get("STAGE_ID")).first(),
        "active": active,
    }

    deal_obj = Deal.objects.update_or_create(ID=data.get("ID"), defaults=deal)
    return deal_obj


def change_deal_active(deal_id, active):
    deal_obj = Deal.objects.filter(ID=deal_id).update(active=active)
    return deal_obj

# stage = Stage.objects.get(STATUS_ID=data["STAGE_ID"])
# deal["CLOSED"] = True if data.get("CLOSED") == "Y" else False
# deal["opportunity"] = data.get("OPPORTUNITY")
# deal["balance_on_payments"] = utils.editing_money_in_number(data.get("UF_CRM_1575629957086", ""))
# deal["amount_paid"] = utils.editing_money_in_number(data.get("UF_CRM_1575375338", ""))
# deal["company"] = Company.objects.filter(ID=data.get("COMPANY_ID")).first()
# deal["direction"] = direction
# deal["stage"] = Stage.objects.get(STATUS_ID=data["STAGE_ID"])
# pprint.pprint(data)
# return
# deal_obj = Deal.objects.update_or_create(deal)
# print("deal = ", deal_obj)

