from . import utils
from dataapp.models import Stage, Deal, Direction, Company
from ..serializers import DealSerializer


def add_deal_drf(deal):
    direction = deal["CATEGORY_ID"]
    if direction in [43, "43"]:
        direction = deal["UF_CRM_1610523951"]

    company_obj = Company.objects.filter(ID=deal.get("COMPANY_ID")).first()
    direction_obj = Direction.objects.filter(ID=direction).first()
    stage_obj = Stage.objects.filter(STATUS_ID=deal.get("STAGE_ID")).first()

    deal["CLOSEDATE"] = deal.get("CLOSEDATE") or None
    deal["CLOSED"] = True if deal.get("CLOSED") == "Y" else False
    deal["opportunity"] = deal.get("OPPORTUNITY") or 0
    deal["balance_on_payments"] = utils.editing_money_in_number(deal.get("UF_CRM_1575629957086", ""))
    deal["amount_paid"] = utils.editing_money_in_number(deal.get("UF_CRM_1575375338", ""))

    deal["company"] =  company_obj.pk if company_obj else None
    deal["direction"] = direction_obj.pk if direction_obj else None
    deal["stage"] = stage_obj.pk if stage_obj else None

    exist_obj = Deal.objects.filter(ID=deal.get("ID", None)).first()

    if exist_obj:
        deal.pop("ID")
        serializer = DealSerializer(exist_obj, data=deal)
    else:
        serializer = DealSerializer(data=deal)

    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as err:
            print(deal.get("ID", None))
            return err
        # return serializer.data
        return

    return serializer.errors


def update_deal_drf(deal):
    if "CATEGORY_ID" in deal:
        direction = deal["CATEGORY_ID"]
        if direction in [43, "43"]:
            direction = deal["UF_CRM_1610523951"]
        direction_obj = Direction.objects.filter(ID=direction).first()
        deal["direction"] = direction_obj.pk if direction_obj else None
    if "COMPANY_ID" in deal:
        company_obj = Company.objects.filter(ID=deal.get("COMPANY_ID")).first()
        deal["company"] =  company_obj.pk if company_obj else None
    if "STAGE_ID" in deal:
        stage_obj = Stage.objects.filter(STATUS_ID=deal.get("STAGE_ID")).first()
        deal["stage"] = stage_obj.pk if stage_obj else None
    if "CLOSEDATE" in deal:
        deal["CLOSEDATE"] = deal.get("CLOSEDATE") or None
    if "CLOSED" in deal:
        deal["CLOSED"] = True if deal.get("CLOSED") == "Y" else False
    if "OPPORTUNITY" in deal:
        deal["opportunity"] = deal.get("OPPORTUNITY") or 0
    if "UF_CRM_1575629957086" in deal:
        deal["balance_on_payments"] = utils.editing_money_in_number(deal.get("UF_CRM_1575629957086", ""))
    if "UF_CRM_1575375338" in deal:
        deal["amount_paid"] = utils.editing_money_in_number(deal.get("UF_CRM_1575375338", ""))

    exist_obj = Deal.objects.filter(ID=deal.get("ID", None)).first()

    if exist_obj:
        deal.pop("ID")
        serializer = DealSerializer(exist_obj, data=deal)
    else:
        serializer = DealSerializer(data=deal)

    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as err:

            return err
        # return serializer.data
        return

    return serializer.errors


# def create_or_update_deal(data, active):
#     direction = data["CATEGORY_ID"]
#     if direction in [43, "43"]:
#         direction = data["UF_CRM_1610523951"]
#
#     deal = {
#         "ID": data.get("ID"),
#         "TITLE": data.get("TITLE"),
#         "DATE_CREATE": data.get("DATE_CREATE") or None,
#         "DATE_MODIFY": data.get("DATE_MODIFY") or None,
#         "CLOSEDATE": data.get("CLOSEDATE") or None,
#         "CLOSED": True if data.get("CLOSED") == "Y" else False,
#         "opportunity": data.get("OPPORTUNITY"),
#         "balance_on_payments": utils.editing_money_in_number(data.get("UF_CRM_1575629957086", "")),
#         "amount_paid": utils.editing_money_in_number(data.get("UF_CRM_1575375338", "")),
#         "company": Company.objects.filter(ID=data.get("COMPANY_ID")).first(),
#         "direction": Direction.objects.filter(ID=direction).first(),
#         "stage": Stage.objects.filter(STATUS_ID=data.get("STAGE_ID")).first(),
#         "active": active,
#     }
#
#     deal_obj = None
#     try:
#         deal_obj = Deal.objects.update_or_create(ID=data.get("ID"), defaults=deal)
#     except Exception as err:
#         print("ID DEAL = ", data.get("ID"))
#         print(err)
#     return deal_obj
#
#
# def change_deal_active(deal_id, active):
#     deal_obj = Deal.objects.filter(ID=deal_id).update(active=active)
#     return deal_obj

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
