import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone


from bitrix24.request import Bitrix24
from dataapp.services import utils, activities


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - USER'
    events = ["ONCRMACTIVITYADD", "ONCRMACTIVITYUPDATE", "ONCRMACTIVITYDELETE"]

    def handle(self, *args, **kwargs):
        self.bx24 = Bitrix24()
        # Получение ID активностей в которых сработало событие в Битрикс24
        for event in self.events:
            activities = self.get_and_save_activities_by_type_event(event)



    def get_and_save_activities_by_type_event(self, event_name, count_recursion=10):
        print(event_name)
        active = False if event_name == "ONCRMACTIVITYDELETE" else True
        if count_recursion <= 0:
            return

        # Получение всех событий
        events_data_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        activities_ids = [event_data_.get("FIELDS", {}).get("ID", {}) for event_data_ in events_data_]
        # activities_ids = [1863, 1867, 1869, 1923, 1925, 485]
        if not activities_ids:
            return
        print("COUNT = ", len(activities_ids))

        if active:
            # Получение данных активностей
            activities_data = activities.get_data_activities(self.bx24, activities_ids)
            if isinstance(activities_data, dict):
                # Получение информации о связанной компании: {<activity_id>: {'COMPANY_ID': <company_id>, 'OWNER_NAME': <title>}, ...}
                companies_data = activities.get_companies_for_activities(self.bx24, activities_data)
                # Сохранение данных
                for activity_id, activity_data in activities_data.items():
                    # print(activity_id)
                    # print(activity_data)
                    activity_obj = activities.create_or_update_activity(activity_data, companies_data.get(activity_id, {}), active)
                    # print(activity_obj)
        else:
            [activities.change_activity_active(activity_id_, active) for activity_id_ in activities_ids]

        # если извлекли не все данные из очереди событий
        if len(activities_ids) == LIMIT_EVENTS:
            self.get_and_save_activities_by_type_event(event_name, count_recursion - 1)

