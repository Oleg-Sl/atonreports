
def get_data_calls(bx24, ids):
    cmd = {}
    for id_ in ids:
        cmd[id_] = f"voximplant.statistic.get?FILTER[CRM_ACTIVITY_ID]={id_}"
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })

    if not response or "result" not in response or "result" not in response["result"]:
        return

    return response["result"]["result"]
