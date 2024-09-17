import redis
from django.core.management.base import BaseCommand

from bitrix24.request import Bitrix24
from dataapp.services import utils, save_deal, get_deals
from dataapp.services.google_sheet import put_deal_to_queu


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - DEAL'
    bx24 = Bitrix24()

    def handle(self, *args, **kwargs):
        save_to_db(self.bx24)


def save_to_db(bx24):
    total_deals = get_total(bx24, "crm.deal.list", {">DATE_CREATE": "2023-06-22"})
    save_deals_to_db(bx24, total_deals)


def save_deals_to_db(bx24, total=0, count=0, id_start=0):
    params = {
        "select": ["*", "UF_*"],
        "filter": {
            ">ID": id_start,
            ">DATE_CREATE": "2023-06-22",
        },
        "order": {"ID": "ASC"},
        "start": -1
    }

    deals_list = bx24.call("crm.deal.list", params).get("result")

    if deals_list and isinstance(deals_list, list):
        count += 50
        fields = bx24.call("crm.deal.fields", {})
        redis_conn = redis.Redis(host='localhost', port=6379, db=5)
        id_start = deals_list[-1].get("ID")
        for deal in deals_list:
            if isinstance(deal, dict):
                put_deal_to_queu.put(deal, fields.get("result", {}), redis_conn, bx24)

        print(f"Получено {count} из {total}")
        save_deals_to_db(bx24, total, count, id_start)


def get_total(bx24, method, filter_field={}):
    params = {
        "FILTER": filter_field,
    }
    response = bx24.call(method, params)
    return response.get("total")

