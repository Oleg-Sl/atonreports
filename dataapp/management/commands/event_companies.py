import pprint
from django.core.management.base import BaseCommand


from bitrix24.request import Bitrix24
from dataapp.services import utils, companies


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - USER'
    events = ["ONCRMCOMPANYADD", "ONCRMCOMPANYUPDATE", "ONCRMCOMPANYDELETE"]

    def handle(self, *args, **kwargs):
        self.bx24 = Bitrix24()

        # Получение ID активностей в которых сработало событие в Битрикс24
        for event in self.events:
            self.get_and_save_companies_by_type_event(event)

    def get_and_save_companies_by_type_event(self, event_name, count_recursion=10):
        print(event_name)
        active = False if event_name == "ONCRMCOMPANYDELETE" else True
        if count_recursion <= 0:
            return

        # Получение всех событий
        events_data_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        pprint.pprint(events_data_)
        companies_ids = [event_data_.get("FIELDS", {}).get("ID", {}) for event_data_ in events_data_]

        if not companies_ids:
            return

        print("COUNT = ", len(companies_ids))
        if active:
            # Получение данных компаний
            companies_data = companies.get_company_data(self.bx24, companies_ids)

            # Получение ИНН компаний {<company_id>: <inn>, ...}
            companies_requisites_data = companies.get_company_requisite(self.bx24, companies_ids)

            # Получение адреса компаний {<company_id>: {'CITY': 'НОВОСИБИРСК', 'PROVINCE': 'НСО', 'REGION': None}, ...}
            companies_requisites_address = companies.get_company_requisite_address(self.bx24, companies_ids)

            # Сохранение данных
            for company_id, company_data in companies_data.items():
                # print(company_id)
                # print(company_data)
                company_obj = companies.create_or_update_company(
                    company_data,
                    companies_requisites_data.get(company_id),
                    companies_requisites_address.get(company_id),
                    active
                )
        else:
            [companies.change_company_active(company_id_, active) for company_id_ in companies_ids]

        # если извлекли не все данные из очереди событий
        if len(companies_ids) == LIMIT_EVENTS:
            self.get_and_save_companies_by_type_event(event_name, count_recursion - 1)
