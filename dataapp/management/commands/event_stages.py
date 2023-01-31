import pprint
from django.core.management.base import BaseCommand


from bitrix24.request import Bitrix24
from dataapp.services import utils, stages


LIMIT_EVENTS = 1


class Command(BaseCommand):
    help = 'Read events - USER'

    def handle(self, *args, **kwargs):
        self.bx24 = Bitrix24()

        # Получение стадий
        stages_data = stages.get_data_stages(self.bx24)

        # Сохранение стадий
        for _, stages_list in stages_data.items():
            for stage_data in stages_list:
                res = stages.create_or_update_stage(stage_data)
