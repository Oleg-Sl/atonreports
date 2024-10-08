from django.core.management.base import BaseCommand

from dataapp.services.save_data_from_bx24 import all_users
from bitrix24.request import Bitrix24


class Command(BaseCommand):
    help = 'Save users to DB'

    def handle(self, *args, **kwargs):
        bx24 = Bitrix24()
        all_users.save_to_db(bx24, "user.get")

