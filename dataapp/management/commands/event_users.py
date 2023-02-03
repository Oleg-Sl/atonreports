import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone


from bitrix24.request import Bitrix24
from dataapp.services import utils
from dataapp.services.users import get_all_users, add_users


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - USER'

    def handle(self, *args, **kwargs):
        bx24 = Bitrix24()
        # Получение ID сделок в которых сработало событие в Битрикс24
        users = utils.get_events(bx24, "ONUSERADD", LIMIT_EVENTS)
        print(users)
        add_users(users)

