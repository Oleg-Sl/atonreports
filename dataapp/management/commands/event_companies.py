import pprint
from django.core.management.base import BaseCommand


from bitrix24.request import Bitrix24
from dataapp.services import utils, save_company, get_companies


LIMIT_EVENTS = 25


class Command(BaseCommand):
    help = 'Read events - COMPANY'
    bx24 = Bitrix24()

    def handle(self, *args, **kwargs):
        print("ONCRMCOMPANYADD")
        self.get_and_save_companies("ONCRMCOMPANYADD")
        print("ONCRMCOMPANYUPDATE")
        self.get_and_save_companies("ONCRMCOMPANYUPDATE")
        print("ONCRMCOMPANYDELETE")
        self.get_and_save_companies("ONCRMCOMPANYDELETE")

    def get_and_save_companies(self, event_name, count_recursion=20):
        if count_recursion <= 0:
            return
        active = False if event_name == "ONCRMCOMPANYDELETE" else True
        events_ = utils.get_events(self.bx24, event_name, LIMIT_EVENTS)
        companies_ids = [event_.get("FIELDS", {}).get("ID", {}) for event_ in events_]
        print("Количество = ", len(companies_ids))
        print(companies_ids)
        if not companies_ids:
            return
        if active:
            # Получение данных компаний
            companies_data = get_companies.get_data(self.bx24, companies_ids)
            # Получение ИНН компаний {<company_id>: <inn>, ...}
            companies_requisites = get_companies.get_requisite(self.bx24, companies_ids)
            # Получение адреса компаний {<company_id>: {'CITY': 'НОВОСИБИРСК', 'PROVINCE': 'НСО', 'REGION': None}, ...}
            companies_address = get_companies.get_address(self.bx24, companies_ids)
            # Сохранение данных
            for company_id, company_data in companies_data.items():
                company_data.update(companies_requisites.get(company_id, {}))
                company_data.update(companies_address.get(company_id, {}))
                print("INPUT: ", company_data)
                res = save_company.update_company_drf(company_data)
                print("OUTPUT: ", res)
        else:
            for company_id_ in companies_ids:
                res = save_company.update_company_drf({
                    "ID": company_id_,
                    "active": active
                })
                print("OUTPUT: ", res)

        # если извлекли не все данные из очереди событий
        if len(companies_ids) == LIMIT_EVENTS:
            self.get_and_save_companies(event_name, count_recursion - 1)
