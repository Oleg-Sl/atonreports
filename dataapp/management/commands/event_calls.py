from django.core.management.base import BaseCommand

from bitrix24.request import Bitrix24
from dataapp.services import utils, save_call


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events: ONVOXIMPLANTCALLEND'
    bx24 = Bitrix24()

    def handle(self, *args, **kwargs):
        print("ONVOXIMPLANTCALLEND")
        self.get_and_save_calls("ONVOXIMPLANTCALLEND")

    def get_and_save_calls(self, event_name, count_recursion=10):
        if count_recursion <= 0:
            return

        # Получение всех событий
        events_calls_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        print("Количество = ", len(events_calls_))
        print(events_calls_)
        if not events_calls_:
            return
        for call_data_ in events_calls_:
            if isinstance(call_data_, dict):
                print("INPUT: ", call_data_)
                res = save_call.add_call_drf(call_data_)
                print("OUTPUT: ", res)

        # если извлекли не все данные из очереди событий
        if len(events_calls_) == LIMIT_EVENTS:
            self.get_and_save_calls(event_name, count_recursion - 1)

