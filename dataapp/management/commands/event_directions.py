from django.core.management.base import BaseCommand
from django.utils import timezone

from bitrix24.request import Bitrix24
from dataapp.services import utils, directions


LIMIT_EVENTS = 1


class Command(BaseCommand):
    help = 'Read events - USER'

    def handle(self, *args, **kwargs):
        self.bx24 = Bitrix24()

        # Получение списка направлений
        directions_data_old = directions.get_directions_old(self.bx24)
        directions_data_new = directions.get_directions_new(self.bx24)

        # Сохранение направлений
        directions.create_or_update(directions_data_old + directions_data_new)
