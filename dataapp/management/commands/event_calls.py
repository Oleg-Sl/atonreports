from django.core.management.base import BaseCommand

from bitrix24.request import Bitrix24
from dataapp.services import utils, save_call, save_activity, get_activities

LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events: ONVOXIMPLANTCALLEND'
    bx24 = Bitrix24()

    def handle(self, *args, **kwargs):
        print("ONVOXIMPLANTCALLEND")
        self.get_and_save_calls("ONVOXIMPLANTCALLEND")

    def get_and_save_calls(self, event_name, count_recursion=20):
        if count_recursion <= 0:
            return

        # Получение всех событий
        events_calls_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        print("Количество = ", len(events_calls_))
        print(events_calls_)
        if not events_calls_:
            return
        activities_ids_ = []
        for call_data_ in events_calls_:
            if isinstance(call_data_, dict):
                activities_ids_.append(call_data_["CRM_ACTIVITY_ID"])
                res = save_call.add_call_drf(call_data_)
                if res:
                    print("INPUT: ", call_data_)
                    print("OUTPUT: ", res)

        self.get_and_save_activities(activities_ids_)
        # если извлекли не все данные из очереди событий
        if len(events_calls_) == LIMIT_EVENTS:
            self.get_and_save_calls(event_name, count_recursion - 1)

    def get_and_save_activities(self, activities_ids_):
        activities_data = get_activities.get_data_activities(self.bx24, activities_ids_)
        if isinstance(activities_data, dict):
            # Получение информации о связанной компании: {<activity_id>: {'COMPANY_ID': <company_id>, 'OWNER_NAME': <title>}, ...}
            companies_data = get_activities.get_companies_for_activities(self.bx24, activities_data)
            for activity_id, activity_data in activities_data.items():
                activity_data.update(companies_data.get(activity_id, {}))
                res = save_activity.update_activity_drf(activity_data)
                if res:
                    print("INPUT: ", activity_data)
                    print("OUTPUT: ", res)



