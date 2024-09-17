from dataapp.models import Activity, Stage, Deal, Direction, User, Company
from ..serializers import ActivitySerializer

from . import get_companies, save_company
from bitrix24.request import Bitrix24


bx24 = Bitrix24()


def get_and_save_company(company_id_):
    if Company.objects.filter(ID=company_id_).exists():
        return
    companies_data_ = get_companies.get_data(bx24, [company_id_])
    if companies_data_ and isinstance(companies_data_, dict) and company_id_ in companies_data_:
        save_company.add_company_drf(companies_data_.get(company_id_, {}))
        print("companies_data = ", companies_data_)


def add_activity_drf(activity):
    if activity.get("COMPANY_ID"):
        get_and_save_company(activity["COMPANY_ID"])

    responsible_obj = User.objects.filter(ID=activity.get("RESPONSIBLE_ID")).first()
    company_obj = Company.objects.filter(ID=activity.get("COMPANY_ID")).first()
    activity["RESPONSIBLE_ID"] = responsible_obj.pk if responsible_obj else None
    activity["COMPANY_ID"] = company_obj.pk if company_obj else None

    exist_obj = Activity.objects.filter(ID=activity.get("ID", None)).first()

    if exist_obj:
        serializer = ActivitySerializer(exist_obj, data=activity)
    else:
        serializer = ActivitySerializer(data=activity)

    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as err:
            return err
        return

    return serializer.errors


def update_activity_drf(activity):
    if "RESPONSIBLE_ID" in activity:
        responsible_obj = User.objects.filter(ID=activity.get("RESPONSIBLE_ID")).first()
        activity["RESPONSIBLE_ID"] = responsible_obj.pk if responsible_obj else None
    if "COMPANY_ID" in activity:
        get_and_save_company(activity["COMPANY_ID"])
        company_obj = Company.objects.filter(ID=activity.get("COMPANY_ID")).first()
        activity["COMPANY_ID"] = company_obj.pk if company_obj else None

    exist_obj = Activity.objects.filter(ID=activity.get("ID", None)).first()

    if exist_obj:
        serializer = ActivitySerializer(exist_obj, data=activity)
    else:
        serializer = ActivitySerializer(data=activity)

    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as err:
            return err
        return

    return serializer.errors
