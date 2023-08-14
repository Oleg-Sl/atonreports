from django.core.management.base import BaseCommand

from dataapp.services.save_data_from_bx24 import all_activities
from bitrix24.request import Bitrix24


class Command(BaseCommand):
    help = 'Save activities to DB'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--datecreatefrom', type=str, help='Стартовая дата для фильтрации по дате добаления, формат: ГГГГ-мм-дд')
        parser.add_argument('-e', '--datecreateto', type=str, help='Конечная дата для фильтрации по дате добаления, формат: ГГГГ-мм-дд')

    def handle(self, *args, **kwargs):
        date_create_from = kwargs['datecreatefrom']
        date_create_to = kwargs['datecreateto']

        bx24 = Bitrix24()

        data = {}
        if date_create_from:
            data[">CREATED"] = date_create_from

        if date_create_to:
            data["<CREATED"] = date_create_to

        all_activities.save_to_db(bx24, data)

