import pprint

from dataapp.models import User


def get_user_obj(bx24, user_id):
    user_obj_ = User.objects.filter(ID=user_id).first()

    if not user_obj_:
        response = bx24.call("user.get", {"ID": user_id})
        user_data_ = response.get("result")
        add_users(user_data_)
        user_obj_ = User.objects.filter(ID=user_id).first()

    return user_obj_


# получение и сохранение всех сотрудников из битрикс
def get_all_users(bx24, filter_data={}):
    response = bx24.call("user.get", filter_data)
    if not response or "result" not in response:
        return
    return response["result"]


# добавление пользователя в БД
def add_users(users):
    for user in users:
        departments = user.get("UF_DEPARTMENT", [])
        User.objects.update_or_create(
            ID=user.get("ID", None),
            LAST_NAME=user.get("LAST_NAME", None),
            NAME=user.get("NAME", None),
            UF_DEPARTMENT=departments[0] if departments else None,
            ACTIVE=user.get("ACTIVE", None)
        )
    return True

