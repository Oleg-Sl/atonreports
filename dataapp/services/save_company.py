from dataapp.models import Activity, Stage, Deal, Direction, User, Company
from ..serializers import CompanySerializer
from django.db import models


def add_company_drf(company):
    assigned_by_id = User.objects.filter(ID=company.get("ASSIGNED_BY_ID")).first()
    company["ASSIGNED_BY_ID"] = assigned_by_id.pk if assigned_by_id else None
    company["sector"] = company.get("UF_CRM_1640828035") or None
    company["region"] = company.get("UF_CRM_1639121988") or None
    company["source"] = company.get("UF_CRM_1639121612") or None
    company["number_employees"] = company.get("UF_CRM_1639121303") or None
    company["district"] = company.get("UF_CRM_1639121341") or None
    company["main_activity"] = company.get("UF_CRM_1617767435") or None
    company["other_activities"] = company.get("UF_CRM_1639121225") or None
    company["profit"] = company.get("UF_CRM_1639121262") or None

    exist_obj = Company.objects.filter(ID=company.get("ID", None)).first()

    if exist_obj:
        serializer = CompanySerializer(exist_obj, data=company)
    else:
        company["date_last_communication"] = "2000-02-06T04:55:58+03:00"
        company["summa_by_company_success"] = 0
        company["summa_by_company_work"] = 0
        serializer = CompanySerializer(data=company)

    if serializer.is_valid():
        serializer.save()
        return serializer.data

    print(serializer.errors)
    return serializer.errors


def update_company_drf(company):
    # if company.get("REGION"):
    if "REGION" in company:
        company["requisite_region"] = company.get("REGION")
    # if company.get("CITY"):
    if "CITY" in company:
        company["requisites_city"] = company.get("CITY")
    # if company.get("PROVINCE"):
    if "PROVINCE" in company:
        company["requisites_province"] = company.get("PROVINCE")
    # if company.get("RQ_INN"):
    if "RQ_INN" in company:
        company["inn"] = company.get("RQ_INN") or ""
    if company.get("active") is not None:
        company["active"] = company.get("active")
    if "ASSIGNED_BY_ID" in company:
        assigned_by_id = User.objects.filter(ID=company.get("ASSIGNED_BY_ID")).first()
        company["ASSIGNED_BY_ID"] = assigned_by_id.pk if assigned_by_id else None
    # if company.get("inn") is not None:
    # if "inn" in company:
    #     company["inn"] = company["inn"] if company["inn"] else ""
    company["inn"] = company.get("inn") if company.get("inn") else ""
    # if company.get("UF_CRM_1640828035") is not None:
    if "UF_CRM_1640828035" in company:
        company["sector"] = company.get("UF_CRM_1640828035") or None
    # if company.get("UF_CRM_1639121988") is not None:
    if "UF_CRM_1639121988" in company:
        company["region"] = company.get("UF_CRM_1639121988") or None
    # if company.get("UF_CRM_1639121612") is not None:
    if "UF_CRM_1639121612" in company:
        company["source"] = company.get("UF_CRM_1639121612") or None
    # if company.get("UF_CRM_1639121303") is not None:
    if "UF_CRM_1639121303" in company:
        company["number_employees"] = company.get("UF_CRM_1639121303") or None
    # if company.get("UF_CRM_1639121341") is not None:
    if "UF_CRM_1639121341" in company:
        company["district"] = company.get("UF_CRM_1639121341") or None
    # if company.get("UF_CRM_1617767435") is not None:
    if "UF_CRM_1617767435" in company:
        company["main_activity"] = company.get("UF_CRM_1617767435") or None
    # if company.get("UF_CRM_1639121225") is not None:
    if "UF_CRM_1639121225" in company:
        company["other_activities"] = company.get("UF_CRM_1639121225") or None
    # if company.get("UF_CRM_1639121262") is not None:
    if "UF_CRM_1639121262" in company:
        company["profit"] = company.get("UF_CRM_1639121262") or None

    exist_obj = Company.objects.filter(ID=company.get("ID", None)).first()
    if exist_obj:
        company["date_last_communication"] = "2000-02-06T04:55:58+03:00"
        company["summa_by_company_success"] = 0
        company["summa_by_company_work"] = 0
        serializer = CompanySerializer(exist_obj, data=company)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
            # return
        return serializer.errors
    else:
        serializer = CompanySerializer(data=company)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
            # return
        return serializer.errors


def change_active_companies(company_id, active):
    return Company.objects.filter(ID=company_id).update(active=active)


def update_companies(companies_ids_bx24):
    companies_ids = Company.objects.values_list("ID", flat=True)
    print(companies_ids)
    print(len(companies_ids))
    count = 0
    for company_id in companies_ids:
        count += 1
        print(count)
        if str(company_id) in companies_ids_bx24:
            continue
        Company.objects.filter(ID=company_id).update(active=False)


def update_companies_dpk():
    companies_ids = Company.objects.values_list("pk", flat=True)
    for company_pk in companies_ids:
        max_call_start_date = Activity.objects.filter(COMPANY_ID=company_pk).aggregate(max_call_date=models.Max('CALL_START_DATE'))["max_call_date"]
        Company.objects.get(ID=company_pk).update(date_last_communication=max_call_start_date.isoformat())
        print(company_pk)

# def create_or_update_company(company_data, inn=None, address={}, active=True):
#     """ Сохранение компании из BX24 """
#     data = {}
#     data["ASSIGNED_BY_ID"] = User.objects.filter(ID=company_data.get("ASSIGNED_BY_ID")).first()
#     data["TITLE"]=company_data.get("TITLE") or None
#     data["DATE_CREATE"]=company_data.get("DATE_CREATE") or None
#     data["ADDRESS"]=company_data.get("ADDRESS") or None
#     data["REVENUE"]=company_data.get("REVENUE") or None
#     data["INDUSTRY"]=company_data.get("INDUSTRY") or None
#     data["sector"]=company_data.get("UF_CRM_1640828035") or None
#     data["region"]=company_data.get("UF_CRM_1639121988") or None
#     data["source"]=company_data.get("UF_CRM_1639121612") or None
#     data["number_employees"]=company_data.get("UF_CRM_1639121303") or None
#     data["district"]=company_data.get("UF_CRM_1639121341") or None
#     data["main_activity"]=company_data.get("UF_CRM_1617767435") or None
#     data["other_activities"]=company_data.get("UF_CRM_1639121225") or None
#     data["profit"]=company_data.get("UF_CRM_1639121262") or None
#     data["requisite_region"] = address.get("REGION") or None
#     data["requisites_city"] = address.get("CITY") or None
#     data["requisites_province"] = address.get("PROVINCE") or None
#     data["inn"] = inn
#     data["active"] = active
#
#     company_obj = Company.objects.update_or_create(ID=company_data.get("ID"), defaults=data)
#     return company_obj
#
#
# def create_or_update_requisite(requisite_data):
#     """ Сохранение ИНН компании из BX24 """
#     company_obj = Company.objects.filter(ID=requisite_data.get("ENTITY_ID")).update(inn=requisite_data.get("RQ_INN"))
#     return company_obj
#
#
# def create_or_update_address(address_data):
#     """ Сохранение адреса компании из BX24 """
#     company_obj = Company.objects.filter(ID=address_data.get("ENTITY_ID")).update(
#         requisite_region=address_data.get("REGION"),
#         requisites_city=address_data.get("CITY"),
#         requisites_province=address_data.get("PROVINCE"),
#     )
#     return company_obj
#
#
# def change_company_active(company_id, active):
#     """ Сохранение компании из BX24 """
#     company_obj = Company.objects.filter(ID=company_id).update(active=active)
#     return company_obj
#
