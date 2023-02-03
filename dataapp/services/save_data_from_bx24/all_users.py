from .. import save_user


def save_to_db(bx24, method, id_start=0):
    params = {
        "filter": {">ID": id_start},
        "order": {"ID": "ASC"},
        "start": -1
    }
    users = bx24.call(method, params).get("result")
    if users and isinstance(users, list):
        id_start = users[-1].get("ID")
        for user in users:
            print("INPUT: ", user)
            res = save_user.add_user_drf(user)
            print("OUTPUT: ", res)
        save_to_db(bx24, method, id_start)
