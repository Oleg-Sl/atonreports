import pprint

from . import utils
from dataapp.models import Activity, User, Phone


def create_or_update_call(call_data):
    data = {
        "CALL_ID": call_data.get("CALL_ID", None),
        "CALL_TYPE": call_data.get("CALL_TYPE", None),
        "PHONE_NUMBER": call_data.get("PHONE_NUMBER", None),
        "CALL_DURATION": call_data.get("CALL_DURATION", None),
        "CALL_START_DATE": call_data.get("CALL_START_DATE", None),
        "CRM_ACTIVITY_ID": Activity.objects.filter(ID=call_data.get("CRM_ACTIVITY_ID")).first(),
        "PORTAL_USER_ID": User.objects.filter(ID=call_data.get("PORTAL_USER_ID")).first(),
    }

    obj_, created = Phone.objects.update_or_create(
        CALL_ID=call_data.get("CALL_ID", None),
        defaults=data
    )
    return obj_
