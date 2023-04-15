
from dataapp.models import Stage, Deal, Direction, Company, User


def put(deal, fields, redis_conn):
    company, stage = Deal.objects.filter(ID=deal["ID"]).values_list("TITLE", "stage__NAME").first()
    deal["company"] = company
    deal["stage"] = stage

    assigned = User.objects.filter(ID=deal["ASSIGNED_BY_ID"]).values("LAST_NAME", "NAME").first()
    deal["assigned"] = f"{assigned['NAME']} {assigned['LAST_NAME']}" if assigned else None

    rop = User.objects.filter(ID=deal["UF_CRM_1529900092"]).values("LAST_NAME", "NAME").first()
    deal["rop"] = f"{rop['NAME']} {rop['LAST_NAME']}" if rop else None

    deal["source"] = get_value(fields["UF_CRM_5DE0B9ADE7595"]["items"])
    deal["source_dir"] = get_value(fields["UF_CRM_5DE0B9ACD162A"]["items"])
    deal["source_id"] = get_value(fields["UF_CRM_SOURCE_ID"]["items"])
    deal["crm_status"] = get_value(fields["UF_CRM_STATUS_ID"]["items"])
    deal["direction"] = get_value(fields["UF_CRM_1610523951"]["items"])

    redis_conn.rpush('googlequeue', deal)


def get_value(items, id_item):
    for item in items:
        if item["ID"] == id_item:
            return item["VALUE"]
