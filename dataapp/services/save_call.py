from dataapp.models import Activity, User, Phone
from ..serializers import PhoneSerializer


def add_call_drf(call):
    activity_obj = Activity.objects.filter(ID=call.get("CRM_ACTIVITY_ID")).first()
    user_obj = User.objects.filter(ID=call.get("PORTAL_USER_ID")).first()

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
        # return serializer.data
        return

    return serializer.errors


# def create_or_update_call(call_data):
#     data = {
#         "CALL_ID": call_data.get("CALL_ID", None),
#         "CALL_TYPE": call_data.get("CALL_TYPE", None),
#         "PHONE_NUMBER": call_data.get("PHONE_NUMBER", None) or None,
#         "CALL_DURATION": call_data.get("CALL_DURATION", None) or None,
#         "CALL_START_DATE": call_data.get("CALL_START_DATE", None) or None,
#         "CRM_ACTIVITY_ID": Activity.objects.filter(ID=call_data.get("CRM_ACTIVITY_ID")).first(),
#         "PORTAL_USER_ID": User.objects.filter(ID=call_data.get("PORTAL_USER_ID")).first(),
#     }
#
#
#     obj_ = None
#     try:
#         obj_, created = Phone.objects.update_or_create(
#             CALL_ID=call_data.get("CALL_ID", None),
#             defaults=data
#         )
#     except Exception as err:
#         print("CALL_ID = ", data.get("CALL_ID"))
#         print(err)
#     return obj_
