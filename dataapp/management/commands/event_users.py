import datetime
from django.core.management.base import BaseCommand

from bitrix24.request import Bitrix24
from dataapp.services import utils, save_user
# from dataapp.services.users import add_user_drf


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - USER'

    def handle(self, *args, **kwargs):
        bx24 = Bitrix24()
        users = utils.get_events(bx24, "ONUSERADD", LIMIT_EVENTS)
        print(datetime.datetime.now())
        for user in users:
            print("INPUT: ", user)
            res_ = save_user.add_user_drf(user)
            print("OUTPUT: ", res_)


