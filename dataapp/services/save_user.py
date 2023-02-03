from dataapp.models import User
from ..serializers import UserSerializer
from .utils import get_url_user

def add_user_orm(user):
    departments = user.get("UF_DEPARTMENT", [])
    User.objects.update_or_create(
        ID=user.get("ID", None),
        LAST_NAME=user.get("LAST_NAME", None),
        NAME=user.get("NAME", None),
        UF_DEPARTMENT=departments[0] if departments else None,
        ACTIVE=user.get("ACTIVE", None),
        URL=get_url_user(user.get("ID", None))
    )


def add_user_drf(user):
    departments = user.get("UF_DEPARTMENT")
    user["URL"] = get_url_user(user.get("ID", None))
    user["UF_DEPARTMENT"] = departments[0] if departments else None,
    exist_obj = User.objects.filter(ID=user.get("ID", None)).first()

    if exist_obj:
        serializer = UserSerializer(exist_obj, data=user)
    else:
        serializer = UserSerializer(data=user)

    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return serializer.errors
