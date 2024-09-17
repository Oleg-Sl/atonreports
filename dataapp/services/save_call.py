from dataapp.models import Activity, User, Phone
from ..serializers import PhoneSerializer


def add_call_drf(call):
    activity_obj = Activity.objects.filter(ID=call.get("CRM_ACTIVITY_ID")).first()
    user_obj = User.objects.filter(ID=call.get("PORTAL_USER_ID")).first()

    call["CALL_DURATION"] = call.get("CALL_DURATION") if call.get("CALL_DURATION") else 0
    call["CRM_ACTIVITY_ID"] = activity_obj.pk if activity_obj else None
    call["PORTAL_USER_ID"] = user_obj.pk if user_obj else None

    exist_obj = Phone.objects.filter(CALL_ID=call.get("CALL_ID", None)).first()

    if exist_obj:
        serializer = PhoneSerializer(exist_obj, data=call)
    else:
        serializer = PhoneSerializer(data=call)

    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as err:
            return err
        return

    return serializer.errors
