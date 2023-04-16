
#
# def get_data(bx24, ids):
#     cmd = {}
#     for id_ in ids:
#         cmd[id_] = f"crm.deal.get?id={id_}"
#     response = bx24.call("batch", {
#         "halt": 0,
#         "cmd": cmd
#     })
#     if not response or "result" not in response or "result" not in response["result"]:
#         return
#
#     return response["result"]["result"]


def get_data(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"crm.deal.list?filter[ID]={id_}&select[]=CATEGORY_ID&select[]=UF_CRM_1610523951&select[]=TITLE&select[]=ID&select[]=DATE_CREATE&select[]=DATE_MODIFY&select[]=CLOSEDATE&select[]=CLOSED&select[]=OPPORTUNITY&select[]=UF_CRM_1575629957086&select[]=UF_CRM_1575375338&select[]=COMPANY_ID&select[]=STAGE_ID&select[]=UF_CRM_WORK_ACCEPTENCE_DAY&select[]=ASSIGNED_BY_ID&select[]=UF_CRM_1529900092&select[]=UF_CRM_1619591604401&select[]=UF_CRM_1620264903&select[]=UF_CRM_1611128441&select[]=UF_CRM_1540262622&select[]=UF_CRM_1581493417&select[]=UF_CRM_1572403036&select[]=UF_CRM_5DE0B9ADE7595&select[]=UF_CRM_5DE0B9ACD162A&select[]=UF_CRM_SOURCE_ID&select[]=UTM_SOURCE&select[]=UTM_CAMPAIGN&select[]=UF_CRM_1611202566&select[]=UF_CRM_1553188396&select[]=UF_CRM_STATUS_ID&select[]=UF_CRM_1526281552&select[]=UF_CRM_1676966362&select[]=UF_CRM_1681619452562"
        # cmd[id_] = f"crm.deal.list?filter[ID]={id_}&select[]=CATEGORY_ID&select[]=UF_CRM_1610523951&select[]=TITLE&select[]=ID&select[]=DATE_CREATE&select[]=DATE_MODIFY&select[]=CLOSEDATE&select[]=CLOSED&select[]=OPPORTUNITY&select[]=UF_CRM_1575629957086&select[]=UF_CRM_1575375338&select[]=COMPANY_ID&select[]=STAGE_ID"
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })
    if not response or "result" not in response or "result" not in response["result"]:
        return

    return response["result"]["result"]
