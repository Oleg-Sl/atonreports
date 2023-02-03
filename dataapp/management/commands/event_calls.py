import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone


from bitrix24.request import Bitrix24
from dataapp.services import utils, calls


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events: ONVOXIMPLANTCALLEND'
    events = ["ONVOXIMPLANTCALLEND", ]

    def handle(self, *args, **kwargs):
        self.bx24 = Bitrix24()

        # Получение завершенных звонков
        for event in self.events:
            self.get_and_save_calls_by_type_event(event)

    def get_and_save_calls_by_type_event(self, event_name, count_recursion=10):
        if count_recursion <= 0:
            return

        # Получение всех событий
        events_call_data_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        # events_call_data_ = self.bx24.call("voximplant.statistic.get", {"SORT": "ID", "ORDER": "DESC"})["result"]

        if not events_call_data_:
            return

        # Сохранение данных
        for call_data_ in events_call_data_[:5]:
            # pprint.pprint(call_data_)
            print(call_data_)
            if isinstance(call_data_, dict):
                print(calls.create_or_update_call(call_data_))

        # если извлекли не все данные из очереди событий
        if len(events_call_data_) == LIMIT_EVENTS:
            self.get_and_save_calls_by_type_event(event_name, count_recursion - 1)

