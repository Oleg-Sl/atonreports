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
            print("ID = ", deal.get("ID", None))
            print("id = ", deal.get("id", None))
            return err
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
        deal["company"] = company_obj.pk if company_obj else None
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
