import datetime
from django.core.management.base import BaseCommand

from dataapp.services.save_data_from_bx24 import get_companies
from dataapp.services import save_company
from bitrix24.request import Bitrix24


class Command(BaseCommand):
    help = 'Update companies to DB'

    def handle(self, *args, **kwargs):
        bx24 = Bitrix24()
        companies_ids = get_companies.get_id_companies_from_bx24(bx24)
        # print(companies_ids)
        print(len(companies_ids))
        save_company.update_companies(companies_ids)

