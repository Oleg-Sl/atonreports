import pprint


from dataapp.models import Direction


def create_or_update(directions_list):
    """ Сохранение всех направлений сделок из BX24 """
    for direction_data in directions_list:
        direction_obj = Direction.objects.update_or_create(**direction_data)


def get_directions_old(bx24):
    """ Влзвращает все направления сделок"""
    entity_type_id = 2    # тип сущности: 2 - сделка
    response = bx24.call(
        "crm.category.list",
        {
            "entityTypeId": entity_type_id
        }
    )
    categories = response.get("result", {}).get("categories", [])

    results = []
    for category in categories:
        results.append({
            "ID": category["id"],
            "VALUE": category["name"],
            "new": False,
            "general_id_bx": category["id"],
        })

    return results


def get_directions_new(bx24):
    """ Возвращвет новые направления с точкой из 43-го """
    response = bx24.call(
        "crm.deal.fields",
        {}
    )
    categories = response.get("result", {}).get("UF_CRM_1610523951", {}).get("items", [])

    results = []
    for category in categories:
        results.append({
            "ID": category["ID"],
            "VALUE": category["VALUE"],
            "new": True,
            "general_id_bx": 43,
        })

    return results

