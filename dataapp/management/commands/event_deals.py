import pprint
from django.core.management.base import BaseCommand


from bitrix24.request import Bitrix24
from dataapp.services import utils, deals


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - USER'
    events = ["ONCRMDEALADD", "ONCRMDEALUPDATE", "ONCRMDEALDELETE"]

    def handle(self, *args, **kwargs):
        self.bx24 = Bitrix24()

        # Получение ID активностей в которых сработало событие в Битрикс24
        for event in self.events:
            self.get_and_save_deals_by_type_event(event)

    def get_and_save_deals_by_type_event(self, event_name, count_recursion=20):
        print(event_name)
        active = False if event_name == "ONCRMDEALDELETE" else True
        if count_recursion <= 0:
            return

        # Получение всех событий
        events_data_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        deals_ids = [event_data_.get("FIELDS", {}).get("ID", {}) for event_data_ in events_data_]

        if not deals_ids:
            return
        print("COUNT = ", len(deals_ids))
        if active:
            # Получение данных сделок
            deals_data = deals.get_data(self.bx24, deals_ids)
            if isinstance(deals_data, dict):
                # Сохранение данных
                for deal_id, deal_data in deals_data.items():
                    # print(deal_id)
                    # print(deal_data)
                    deals.create_or_update_deal(deal_data, active)
        else:
            [deals.change_deal_active(deals_id_, active) for deals_id_ in deals_ids]

        # если извлекли не все данные из очереди событий
        if len(deals_ids) == LIMIT_EVENTS:
            self.get_and_save_deals_by_type_event(event_name, count_recursion - 1)
