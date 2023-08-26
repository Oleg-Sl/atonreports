import sys
sys.setrecursionlimit(10000)


def get_id_companies_from_bx24(bx24, id_start=0):
    params = {
        "select": ["ID"],
        "filter": {">ID": id_start},
        "order": {"ID": "ASC"},
        "start": -1
    }

    companies_list = bx24.call("crm.company.list", params).get("result")

    companies_ids = []
    if companies_list and isinstance(companies_list, list):
        id_start = companies_list[-1].get("ID")
        companies_ids.extend([company.get("ID") for company in companies_list])
        print("===>>> ", id_start)
        companies_ids.extend(get_id_companies_from_bx24(bx24, id_start))

    return companies_ids
