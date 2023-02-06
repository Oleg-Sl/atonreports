import calendar
import datetime
from django.core.cache import cache
from collections import Counter
from django.db import models

from dataapp.models import (
    User,
    Direction,
    Stage,
    Company,
    Deal,
    Activity,
    Phone,
    ProductionCalendar,
    CallsPlan,
    Comment
)
from ..serializers import ProductionCalendarSerializer

CASH_TIMMEOUT = 6
# 0 * 60 * 4


# добавление всех дней месяц в БД
def create_calendar(year, month):
    # количество дней в месяце
    count_days = calendar.monthrange(int(year), int(month))[1]
    # список объектов с датами для создания календаря в БД
    calendar_days_list = [{"date_calendar": datetime.date(year, month, day)} for day in range(1, count_days + 1)]
    serializer = ProductionCalendarSerializer(data=calendar_days_list, many=True)
    if serializer.is_valid():
        serializer.save()
        return True, serializer.data
    return False, serializer.errors


def get_users_by_depeartments(departments):
    departs_str = ','.join([str(i) for i in sorted(departments)])
    key = f"users_departs_{departs_str}"
    users = cache.get(key)
    if users is None:
        users = User.objects.only(
            "UF_DEPARTMENT",
            "ACTIVE",
            "STATUS_DISPLAY",
            "ID", "LAST_NAME", "NAME"
        ).filter(
            UF_DEPARTMENT__in=departments,
            ACTIVE=True,
            STATUS_DISPLAY=True,
        ).values(
            "ID", "LAST_NAME", "NAME", "UF_DEPARTMENT"
        ).order_by("LAST_NAME", "NAME")
        cache.set(key, users, CASH_TIMMEOUT)

    return users


def get_calls_by_month(departments, year, duration):
    departs_str = ','.join([str(i) for i in sorted(departments)])
    key = f"calls_departs_{departs_str}_year_{year}"
    calls = cache.get(key)
    now = datetime.datetime.now()
    if calls is None:
        queryset_calls = Activity.objects.select_related("RESPONSIBLE_ID").only(
            "active",
            "DURATION",
            "DIRECTION",
            "TYPE_ID",
            "CALL_START_DATE",
            "RESPONSIBLE_ID__STATUS_DISPLAY",
            "RESPONSIBLE_ID__ACTIVE",
            "RESPONSIBLE_ID__UF_DEPARTMENT"
        ).filter(
            COMPANY_ID__isnull=False,
            RESPONSIBLE_ID__UF_DEPARTMENT__in=departments,
            RESPONSIBLE_ID__ACTIVE=True,
            RESPONSIBLE_ID__STATUS_DISPLAY=True,
            # phone__CALL_START_DATE__year=year,
            CALL_START_DATE__year=year,
            TYPE_ID=2,
            DIRECTION=2,
            # phone__CALL_DURATION__gte=duration,
            DURATION__gte=duration,
            active=True
        ).distinct(
            'RESPONSIBLE_ID__ID', 'CALL_START_DATE__month', 'CALL_START_DATE__day', 'COMPANY_ID'
        ).values_list(
            # "RESPONSIBLE_ID", 'phone__CALL_START_DATE__month'
            "RESPONSIBLE_ID__ID", 'CALL_START_DATE__month'
        )
        calls = Counter(queryset_calls)
        cache.set(key, calls, CASH_TIMMEOUT)
    elif year == now.year or str(year) == str(now.year):
        queryset_calls = Activity.objects.select_related("RESPONSIBLE_ID").only(
            "active",
            "DURATION",
            "DIRECTION",
            "TYPE_ID",
            "CALL_START_DATE",
            "RESPONSIBLE_ID__STATUS_DISPLAY",
            "RESPONSIBLE_ID__ACTIVE",
            "RESPONSIBLE_ID__UF_DEPARTMENT"
        ).filter(
            RESPONSIBLE_ID__UF_DEPARTMENT__in=departments,
            RESPONSIBLE_ID__ACTIVE=True,
            RESPONSIBLE_ID__STATUS_DISPLAY=True,
            # phone__CALL_START_DATE__year=year,
            CALL_START_DATE__year=year,
            # phone__CALL_START_DATE__month=now.month,
            CALL_START_DATE__month=now.month,
            TYPE_ID=2,
            DIRECTION=2,
            # phone__CALL_DURATION__gte=duration,
            DURATION__gte=duration,
            active=True
        ).distinct(
            'RESPONSIBLE_ID__ID', 'CALL_START_DATE__month', 'CALL_START_DATE__day', 'COMPANY_ID'
        ).values_list(
            # "RESPONSIBLE_ID", 'phone__CALL_START_DATE__month'
            "RESPONSIBLE_ID__ID", 'CALL_START_DATE__month'
        )
        calls_new = Counter(queryset_calls)
        # calls.update(calls_new)
        calls = update_dict(calls, calls_new)

    return calls


def get_meetings_by_month(departments, year):
    meetings = Activity.objects.select_related("RESPONSIBLE_ID").only(
            "END_TIME",
            "TYPE_ID",
            "active",
            "COMPLETED",
            "RESPONSIBLE_ID__STATUS_DISPLAY",
            "RESPONSIBLE_ID__ACTIVE",
            "RESPONSIBLE_ID__UF_DEPARTMENT"
        ).filter(
        RESPONSIBLE_ID__UF_DEPARTMENT__in=departments,
        RESPONSIBLE_ID__ACTIVE=True,
        RESPONSIBLE_ID__STATUS_DISPLAY=True,
        END_TIME__year=year,
        TYPE_ID=1,
        active=True,
        COMPLETED="Y"
    ).values(
        "RESPONSIBLE_ID__ID", 'END_TIME__month'
    ).annotate(
        counts=models.Count('END_TIME')
    )

    return meetings


def get_calls_by_day(departments, year, month, duration):
    departs_str = ','.join([str(i) for i in sorted(departments)])
    key = f"calls_departs_{departs_str}_year_{year}_month_{month}"
    calls = cache.get(key)
    now = datetime.datetime.now()
    if calls is None:
        queryset_calls = Activity.objects.select_related("RESPONSIBLE_ID").only(
            "COMPANY_ID",
            "active",
            "DURATION",
            "DIRECTION",
            "TYPE_ID",
            "CALL_START_DATE",
            "RESPONSIBLE_ID__ID",
            "RESPONSIBLE_ID__STATUS_DISPLAY",
            "RESPONSIBLE_ID__ACTIVE",
            "RESPONSIBLE_ID__UF_DEPARTMENT"
        ).filter(
            COMPANY_ID__isnull=False,
            RESPONSIBLE_ID__UF_DEPARTMENT__in=departments,
            RESPONSIBLE_ID__ACTIVE=True,
            RESPONSIBLE_ID__STATUS_DISPLAY=True,
            # phone__CALL_START_DATE__year=year,
            CALL_START_DATE__year=year,
            # phone__CALL_START_DATE__month=month,
            CALL_START_DATE__month=month,
            TYPE_ID=2,
            DIRECTION=2,
            # phone__CALL_DURATION__gte=duration,
            DURATION__gte=duration,
            active=True
        ).distinct(
            'RESPONSIBLE_ID__ID', 'CALL_START_DATE__day', 'COMPANY_ID__ID'
            # 'RESPONSIBLE_ID__ID', 'CALL_START_DATE__month', 'CALL_START_DATE__day', 'COMPANY_ID__ID'
        ).values_list(
            # "RESPONSIBLE_ID", 'phone__CALL_START_DATE__day'
            "RESPONSIBLE_ID__ID", 'CALL_START_DATE__day'
        )
        calls = Counter(queryset_calls)
        cache.set(key, calls, CASH_TIMMEOUT)
    elif str(year) == str(now.year) and str(month) == str(now.month):
        queryset_calls = Activity.objects.select_related("RESPONSIBLE_ID").only(
            "COMPANY_ID",
            "active",
            "DURATION",
            "DIRECTION",
            "TYPE_ID",
            "CALL_START_DATE",
            "RESPONSIBLE_ID__ID",
            "RESPONSIBLE_ID__STATUS_DISPLAY",
            "RESPONSIBLE_ID__ACTIVE",
            "RESPONSIBLE_ID__UF_DEPARTMENT"
        ).filter(
            COMPANY_ID__isnull=False,
            RESPONSIBLE_ID__UF_DEPARTMENT__in=departments,
            RESPONSIBLE_ID__ACTIVE=True,
            RESPONSIBLE_ID__STATUS_DISPLAY=True,
            # phone__CALL_START_DATE__year=year,
            # phone__CALL_START_DATE__month=month,
            # phone__CALL_START_DATE__day=now.day,
            CALL_START_DATE__year=year,
            CALL_START_DATE__month=month,
            CALL_START_DATE__day=now.day,
            TYPE_ID=2,
            DIRECTION=2,
            # phone__CALL_DURATION__gte=duration,
            DURATION__gte=duration,
            active=True
        ).distinct(
            'RESPONSIBLE_ID__ID', 'CALL_START_DATE__day', 'COMPANY_ID__ID'
            # 'RESPONSIBLE_ID__ID', 'CALL_START_DATE__day', 'COMPANY_ID'
        ).values_list(
            # "RESPONSIBLE_ID", 'phone__CALL_START_DATE__day'
            "RESPONSIBLE_ID__ID", 'CALL_START_DATE__day'
        )
        calls_new = Counter(queryset_calls)
        # calls.update(calls_new)
        calls = update_dict(calls, calls_new)

    return calls


def get_meetings_by_day(departments, year, month):
    meetings = Activity.objects.select_related("RESPONSIBLE_ID").only(
            "END_TIME",
            "TYPE_ID",
            "active",
            "COMPLETED",
            "RESPONSIBLE_ID__STATUS_DISPLAY",
            "RESPONSIBLE_ID__ACTIVE",
            "RESPONSIBLE_ID__UF_DEPARTMENT"
        ).filter(
        RESPONSIBLE_ID__UF_DEPARTMENT__in=departments,
        RESPONSIBLE_ID__ACTIVE=True,
        RESPONSIBLE_ID__STATUS_DISPLAY=True,
        END_TIME__year=year,
        END_TIME__month=month,
        TYPE_ID=1,
        active=True,
        COMPLETED="Y"
    ).values(
        "RESPONSIBLE_ID__ID", 'END_TIME__day'
    ).annotate(
        counts=models.Count('END_TIME')
    )

    return meetings


def update_dict(dict_old, dict_new):
    for key, val in dict_new.items():
        dict_old[key] = val
    return dict_old

