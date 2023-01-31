import pprint


from bitrix24.request import Bitrix24
from .. import directions


def create_or_update_directions():
    bx24 = Bitrix24()

    # Получение списка направлений
    directions_data_old = directions.get_directions_old(bx24)
    directions_data_new = directions.get_directions_new(bx24)

    # Сохранение направлений
    directions.create_or_update(directions_data_old + directions_data_new)
