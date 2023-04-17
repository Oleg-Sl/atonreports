import json
from dataapp.models import Stage, Deal, Direction, Company, User


def put(deal, fields, redis_conn):
    # company, stage = Deal.objects.filter(ID=deal["ID"]).values_list("TITLE", "stage__NAME").first()
    # deal["company"] = company
    # deal["stage"] = stage

    if deal["CATEGORY_ID"] and deal["CATEGORY_ID"] not in [43, "43"]:
        return

    if deal["UF_CRM_1602484766"] and int(deal.get("UF_CRM_1602484766")) <= 4:
        return

    # COMPANY_ID
    company = Company.objects.filter(ID=deal["COMPANY_ID"]).values("TITLE").first()
    deal["company"] = company['TITLE'] if company else None

    stage = Stage.objects.filter(STATUS_ID=deal["STAGE_ID"]).values("NAME", "status").first()
    deal["stage"] = stage['NAME'] if stage else None
    deal["deal_won"] = False if stage and stage['status'] == "FAILURE" else True

    assigned = User.objects.filter(ID=deal["ASSIGNED_BY_ID"]).values("LAST_NAME", "NAME").first()
    deal["assigned"] = f"{assigned['NAME']} {assigned['LAST_NAME']}" if assigned else None

    rop = User.objects.filter(ID=deal["UF_CRM_1529900092"]).values("LAST_NAME", "NAME").first()
    deal["rop"] = f"{rop['NAME']} {rop['LAST_NAME']}" if rop else None

    deal["source"] = get_value(fields["UF_CRM_5DE0B9ADE7595"]["items"], deal["UF_CRM_5DE0B9ADE7595"])
    deal["source_dir"] = get_value(fields["UF_CRM_5DE0B9ACD162A"]["items"], deal["UF_CRM_5DE0B9ACD162A"])
    deal["source_id"] = get_value(fields["UF_CRM_SOURCE_ID"]["items"], deal["UF_CRM_SOURCE_ID"])
    deal["crm_status"] = get_value(fields["UF_CRM_STATUS_ID"]["items"], deal["UF_CRM_STATUS_ID"])
    deal["direction"] = get_value(fields["UF_CRM_1610523951"]["items"], deal["UF_CRM_1610523951"])

    deal_str = json.dumps(deal)
    redis_conn.rpush('googlequeue', deal_str)


def get_value(items, id_item):
    for item in items:
        if item["ID"] == id_item:
            return item["VALUE"]
