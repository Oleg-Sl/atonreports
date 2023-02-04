

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
