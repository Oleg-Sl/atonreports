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
        print("ONCRMDEALADD")
        self.get_and_save_deals("ONCRMDEALADD")
        print("ONCRMDEALUPDATE")
        self.get_and_save_deals("ONCRMDEALUPDATE")
        print("ONCRMDEALDELETE")
        self.get_and_save_deals("ONCRMDEALDELETE")

    def get_and_save_deals(self, event_name, count_recursion=40):
        if count_recursion <= 0:
            return

        active = False if event_name == "ONCRMDEALDELETE" else True
        events_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        deals_ids = [event_.get("FIELDS", {}).get("ID", {}) for event_ in events_]
        print("Количество = ", len(deals_ids))
        print(deals_ids)
        if not deals_ids:
            return
        if active:
            redis_conn = redis.Redis(host='localhost', port=6379, db=5)
            deals_data = get_deals.get_data(self.bx24, deals_ids)
            fields = self.bx24.call("crm.deal.fields", {})
            if isinstance(deals_data, dict):
                for deal_id, deal_data in deals_data.items():
                    if deal_data:
                        print("deal_id: ", deal_id)
                        print("deal_data: ", deal_data)
                        put_deal_to_queu.put(deal_data[0], fields.get("result", {}), redis_conn, self.bx24)
                        res = save_deal.update_deal_drf(deal_data[0])
                        if res:
                            print("INPUT: ", deal_data)
                            print("OUTPUT: ", res)
        else:
            for deal_id_ in deals_ids:
                res = save_deal.update_deal_drf({
                    "ID": deal_id_,
                    "active": active
                })
                if res:
                    print("OUTPUT: ", res)

        # если извлекли не все данные из очереди событий
        if len(deals_ids) == LIMIT_EVENTS:
            self.get_and_save_deals(event_name, count_recursion - 1)
