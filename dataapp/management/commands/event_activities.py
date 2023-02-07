from django.core.management.base import BaseCommand

from bitrix24.request import Bitrix24
from dataapp.services import utils, save_activity, get_activities, get_calls, save_call


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - ACTIVITY'
    bx24 = Bitrix24()

    def handle(self, *args, **kwargs):
        print("ONCRMACTIVITYADD")
        self.get_and_save_activities("ONCRMACTIVITYADD")
        print("ONCRMACTIVITYUPDATE")
        self.get_and_save_activities("ONCRMACTIVITYUPDATE")
        # print("ONCRMACTIVITYDELETE")
        # self.get_and_save_activities("ONCRMACTIVITYDELETE")

    def get_and_save_activities(self, event_name, count_recursion=40):
        if count_recursion <= 0:
            return

        active = False if event_name == "ONCRMACTIVITYDELETE" else True
        events_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        activities_ids = [event_.get("FIELDS", {}).get("ID", {}) for event_ in events_]
        print("Количество = ", len(activities_ids))
        print(activities_ids)
        if not activities_ids:
            return
        if active:
            activities_data = get_activities.get_data_activities(self.bx24, activities_ids)
            if isinstance(activities_data, dict):
                # Получение информации о связанной компании: {<activity_id>: {'COMPANY_ID': <company_id>, 'OWNER_NAME': <title>}, ...}
                companies_data = get_activities.get_companies_for_activities(self.bx24, activities_data)
                for activity_id, activity_data in activities_data.items():
                    activity_data.update(companies_data.get(activity_id, {}))
                    res = save_activity.update_activity_drf(activity_data)
                    if res:
                        print("INPUT: ", activity_data)
                        print("OUTPUT: ", res)

            calls_data = get_calls.get_data_calls(self.bx24, activities_ids)
            if isinstance(calls_data, dict):
                for _, call_data_ in calls_data.items():
                    if not call_data_:
                        continue
                    res = save_call.add_call_drf(call_data_)
                    if res:
                        print("INPUT: ", call_data_)
                        print("OUTPUT: ", res)

        else:
            for activity_id_ in activities_ids:
                res = save_activity.update_activity_drf({
                    "ID": activity_id_,
                    "active": active
                })
                if res:
                    print("OUTPUT: ", res)

        # если извлекли не все данные из очереди событий
        if len(activities_ids) == LIMIT_EVENTS:
            self.get_and_save_activities(event_name, count_recursion - 1)
