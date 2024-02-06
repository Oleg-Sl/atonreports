import pprint

from dataapp.models import Activity, Stage, Deal, Direction, User, Company


def get_data_stages(bx24):
    cmd = {}
    directions_list = Direction.objects.all()
    for directions_obj in directions_list:
        cmd[directions_obj.ID] = f"crm.status.list?filter[CATEGORY_ID]={directions_obj.ID}"

    cmd["0"] = f"crm.status.list?filter[ENTITY_ID]=DEAL_STAGE"

    response = bx24.call("batch", {
        "halt": 0,
        "cmd": cmd
    })

    if not response or "result" not in response or "result" not in response["result"]:
        return {}

    return response["result"]["result"]


def create_or_update_stage(stage_data):
    """ Сохранение всех стадий переданного направления сделки из BX24 """
    data = {
        "STATUS_ID": stage_data.get("STATUS_ID"),
        "NAME": stage_data.get("NAME"),
        "direction": Direction.objects.filter(ID=stage_data.get("CATEGORY_ID")).first(),
        # won = True,
        # status = "WORK",
    }
    stage_obj, created = Stage.objects.update_or_create(
        ID=stage_data.get("ID"),
        defaults=data
    )
    return stage_obj
