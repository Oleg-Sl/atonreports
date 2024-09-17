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
    if "REGION" in company:
        company["requisite_region"] = company.get("REGION")
    if "CITY" in company:
        company["requisites_city"] = company.get("CITY")
    if "PROVINCE" in company:
        company["requisites_province"] = company.get("PROVINCE")
    if "RQ_INN" in company:
        company["inn"] = company.get("RQ_INN") or ""
    if company.get("active") is not None:
        company["active"] = company.get("active")
    if "ASSIGNED_BY_ID" in company:
        assigned_by_id = User.objects.filter(ID=company.get("ASSIGNED_BY_ID")).first()
        company["ASSIGNED_BY_ID"] = assigned_by_id.pk if assigned_by_id else None
    company["inn"] = company.get("inn") if company.get("inn") else ""
    if "UF_CRM_1640828035" in company:
        company["sector"] = company.get("UF_CRM_1640828035") or None
    if "UF_CRM_1639121988" in company:
        company["region"] = company.get("UF_CRM_1639121988") or None
    if "UF_CRM_1639121612" in company:
        company["source"] = company.get("UF_CRM_1639121612") or None
    if "UF_CRM_1639121303" in company:
        company["number_employees"] = company.get("UF_CRM_1639121303") or None
    if "UF_CRM_1639121341" in company:
        company["district"] = company.get("UF_CRM_1639121341") or None
    if "UF_CRM_1617767435" in company:
        company["main_activity"] = company.get("UF_CRM_1617767435") or None
    if "UF_CRM_1639121225" in company:
        company["other_activities"] = company.get("UF_CRM_1639121225") or None
    if "UF_CRM_1639121262" in company:
        company["profit"] = company.get("UF_CRM_1639121262") or None

    exist_obj = Company.objects.filter(ID=company.get("ID", None)).first()
    if exist_obj:
        serializer = CompanySerializer(exist_obj, data=company)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors
    else:
        company["date_last_communication"] = "2000-02-06T04:55:58+03:00"
        company["summa_by_company_success"] = 0
        company["summa_by_company_work"] = 0
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
        if max_call_start_date:
            Company.objects.filter(pk=company_pk).update(date_last_communication=max_call_start_date.isoformat())
            print(company_pk)
