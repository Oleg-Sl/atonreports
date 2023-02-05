
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
        cmd[id_] = f"crm.deal.list?filter[id]={id_}&select[]=CATEGORY_ID&select[]=UF_CRM_1610523951&select[]=TITLE&select[]=ID&select[]=DATE_CREATE&select[]=DATE_MODIFY&select[]=CLOSEDATE&select[]=CLOSED&select[]=OPPORTUNITY&select[]=UF_CRM_1575629957086&select[]=UF_CRM_1575375338&select[]=COMPANY_ID&select[]=STAGE_ID"
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })
    if not response or "result" not in response or "result" not in response["result"]:
        return

    return response["result"]["result"]
