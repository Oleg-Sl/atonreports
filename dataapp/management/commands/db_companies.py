import datetime
from django.core.management.base import BaseCommand

from dataapp.services.save_data_from_bx24 import all_companies
from bitrix24.request import Bitrix24


class Command(BaseCommand):
    help = 'Save companies to DB'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--datecreatefrom', type=str, help='Стартовая дата для фильтрации по дате добаления, формат: ГГГГ-мм-дд')
        parser.add_argument('-e', '--datecreateto', type=str, help='Конечная дата для фильтрации по дате добаления, формат: ГГГГ-мм-дд')

    def handle(self, *args, **kwargs):
        date_create_from = kwargs['datecreatefrom']
        date_create_to = kwargs['datecreateto']
        if not date_create_from or not date_create_to:
            return "Отсутствуют данные для фильтрации!!!"

        print(f"{date_create_from=}")
        print(f"{date_create_to=}")

        bx24 = Bitrix24()
        all_companies.save_to_db(bx24, date_create_from, date_create_to)

