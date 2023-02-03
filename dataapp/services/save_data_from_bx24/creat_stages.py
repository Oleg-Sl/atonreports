import pprint

from bitrix24.request import Bitrix24
from .. import stages


def create_or_update_stages():
    bx24 = Bitrix24()

    # Получение стадий
    stages_data = stages.get_data_stages(bx24)

    # Сохранение стадий
    for _, stages_list in stages_data.items():
        for stage_data in stages_list:
            res = stages.create_or_update_stage(stage_data)
