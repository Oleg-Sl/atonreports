import datetime
from django.core.management.base import BaseCommand

from dataapp.services.save_data_from_bx24 import all_companies
from bitrix24.request import Bitrix24



class Command(BaseCommand):
    help = 'Save companies to DB'

    def handle(self, *args, **kwargs):
        bx24 = Bitrix24()

        all_companies.save_to_db(bx24, datetime.date(2023, 3, 10))


