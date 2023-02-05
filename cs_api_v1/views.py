from rest_framework import views, viewsets, filters, status, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from django_filters import rest_framework as filters_drf


from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

import os
import logging
import json
import time
import datetime
import calendar
from collections import Counter




# from . import service, bitrix24
from . import filter_queryset
from .services import common
from bitrix24 import tokens

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

from .serializers import (
#     ActivityFullSerializer,
#     CallsSerializer,
    UsersUpdateSerializer,
    ActivitySerializer,
    CommentSerializer,
    ProductionCalendarSerializer,
    CallsPlanSerializer,
#     UsersSerializer,
)


CASH_TIMMEOUT = 60 * 60 * 4


# Обработчик установки приложения
class InstallApiView(views.APIView):
    # permission_classes = [AllowAny]

    @xframe_options_exempt
    def post(self, request):
        data = {
            "domain": request.query_params.get("DOMAIN", "bits24.bitrix24.ru"),
            "auth_token": request.data.get("AUTH_ID", ""),
            "expires_in": request.data.get("AUTH_EXPIRES", 3600),
            "refresh_token": request.data.get("REFRESH_ID", ""),
            # используется для проверки достоверности событий Битрикс24
            "application_token": request.query_params.get("APP_SID", ""),
            'client_endpoint': f'https://{request.query_params.get("DOMAIN", "bits24.bitrix24.ru")}/rest/',
        }
        # print("data = ", data)
        tokens.save_secrets(data)
        return render(request, 'calls-statistic/install.html')


# Обработчик установленного приложения
class IndexApiView(views.APIView):
    # permission_classes = [AllowAny]

    @xframe_options_exempt
    def post(self, request):
        return render(request, 'calls-statistic/index.html', context={
            "DOMAIN": "https://otchet.atonlab.ru/reports/"
        })


# # Обработчик удаления приложения
# class AppUnistallApiView(views.APIView):
#     permission_classes = [AllowAny]
#
#     @xframe_options_exempt
#     def post(self, request):
#         return Response(status.HTTP_200_OK)


class UsersDataFilter(filters_drf.FilterSet):
    class Meta:
        model = User
        fields = ["UF_DEPARTMENT", "ALLOWED_EDIT", "ALLOWED_SETTING", ]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(ACTIVE=True).order_by("LAST_NAME", "NAME")
    serializer_class = UsersUpdateSerializer
    filter_backends = [filters_drf.DjangoFilterBackend]
    filterset_class = UsersDataFilter
    lookup_field = 'ID'
    # permission_classes = [IsAuthenticated]

    # @method_decorator(cache_page(CASH_TIMMEOUT))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# Получение звоков за выбранный период
class CallsViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.filter(
        COMPANY_ID__isnull=False,
        TYPE_ID=2,      # только звонки
        DIRECTION=2,    # только исходящие
        active=True
    ).distinct(
        'CALL_START_DATE__month', 'CALL_START_DATE__day', 'COMPANY_ID'
    ).order_by(
        'CALL_START_DATE__month', 'CALL_START_DATE__day', 'COMPANY_ID', 'CALL_START_DATE'
    )
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = filter_queryset.CallsFilter
    lookup_field = 'ID'
    # permission_classes = [IsAuthenticated]


# Получение, добавление, обновление комментариев
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    ordering = ["date_comment_add"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = filter_queryset.CommentFilter
    # permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        recipient = User.objects.filter(ID=request.data.get("recipient")).first()
        commentator = User.objects.filter(ID=request.data.get("commentator")).first()
        verified_by_user = User.objects.filter(ID=request.data.get("verified_by_user")).first()
        data = {
            # "recipient": request.data.get("recipient", instance.recipient.pk),
            "recipient": recipient or instance.recipient,
            # "commentator": request.data.get("commentator", instance.commentator.pk),
            "commentator": commentator or instance.commentator,
            "date_comment": request.data.get("date_comment", instance.date_comment),
            "date_comment_add": request.data.get("date_comment_add", instance.date_comment_add),
            "comment": request.data.get("comment", instance.comment),
            "verified": request.data.get("verified", instance.verified),
            # "verified_by_user": request.data.get("verified_by_user", instance.verified_by_user),
            "verified_by_user": verified_by_user or instance.verified_by_user,
            "date_verified": request.data.get("date_verified", instance.date_verified)
        }

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# Добавление и изменение производственного календаря - NEW
class ProductionCalendarViewSet(views.APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, requests):
        year = requests.query_params.get("year", datetime.datetime.now().year)
        status_day = requests.query_params.get("status", "work")

        queryset = ProductionCalendar.objects.filter(
            date_calendar__year=year, status=status_day
        ).annotate(
            month=models.functions.Extract("date_calendar", "month"),
            day=models.functions.Extract("date_calendar", "day"),
        )

        result = ProductionCalendarSerializer(queryset, many=True)

        data = {}
        for obj in result.data:
            month = obj["month"]
            if not data.get(month, None):
                data[month] = []
            data[month].append(obj["day"])

        return Response(data, status=status.HTTP_200_OK)

    def post(self, requests):
        date_str = requests.data.get("date_calendar", None)

        if not date_str:
            return Response('"date_calendar": обязательное поле', status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            year = date.year
            month = date.month
            day = date.day
        except ValueError:
            return Response('"date_calendar": не правильный формат даты, требуется формат "гггг-мм-дд"',
                            status=status.HTTP_400_BAD_REQUEST)

        calendar_exist = ProductionCalendar.objects.filter(date_calendar=date).exists()

        if not calendar_exist:
            # при отсутствии календаря его создание
            status_calendar, data_calendar = common.create_calendar(year, month)
            if not status_calendar:
                return Response(data_calendar, status=status.HTTP_400_BAD_REQUEST)

        calendar_day = ProductionCalendar.objects.filter(date_calendar=date).first()

        if not calendar_day:
            return Response("Failed to create calendar", status=status.HTTP_400_BAD_REQUEST)

        # изменение статуса дня
        serializer = ProductionCalendarSerializer(calendar_day, data=requests.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Добавление и изменение плана по звонкам - NEW
class CallsPlanViewSet(views.APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, requests):
        year = requests.query_params.get("year", datetime.datetime.now().year)

        queryset = CallsPlan.objects.filter(calendar__date_calendar__year=year, calendar__date_calendar__day=1). \
            annotate(month=models.functions.Extract("calendar__date_calendar", "month"))

        serializer = CallsPlanSerializer(queryset, many=True)

        data = [{} for _ in range(12)]
        for item in serializer.data:
            index = item["month"] - 1
            employee = str(item["employee"])
            data[index][employee] = item["count_calls"]

        return Response(data, status=status.HTTP_200_OK)

    def post(self, requests):
        calendar_date = requests.data.get("calendar", None)  # дата: гггг-мм-дд
        employee = requests.data.get("employee", None)  # ID работника
        count_calls = requests.data.get("count_calls", None)  # количество звонков - план
        all_month = requests.data.get("all_month", True)  # обновить план на весь месяц или один день

        if not calendar_date:
            return Response('"calendar": обязательное поле', status=status.HTTP_400_BAD_REQUEST)

        if not employee:
            return Response('"employee": обязательное поле', status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.datetime.strptime(calendar_date, "%Y-%m-%d")
            year = date.year
            month = date.month
            day = date.day
        except ValueError:
            return Response('"calendar": не правильный формат даты, требуется формат "гггг-мм-дд"',
                            status=status.HTTP_400_BAD_REQUEST)

        # получение производственного календаря
        calendar_exist = ProductionCalendar.objects.filter(date_calendar=date).exists()

        # создание производственного календаря за переданный месяц, при его отсутствиии
        if not calendar_exist:
            # при отсутствии календаря - его создание
            status_calendar, data_calendar = common.create_calendar(year, month)
            if not status_calendar:
                return Response(data_calendar, status=status.HTTP_400_BAD_REQUEST)

        # получение записи плана по звонкам пользователя за переданный день
        calls_plan_exists = CallsPlan.objects.filter(calendar__date_calendar=date, employee__ID=employee).exists()

        # если запись отсутствует - создание записей по звонкам за месяц
        if not calls_plan_exists:
            prod_calendar = ProductionCalendar.objects.filter(
                date_calendar__year=year,
                date_calendar__month=month
            )
            calls_plan_list = [{"calendar": obj_prod_calend.pk, "employee": employee} for obj_prod_calend in
                               prod_calendar]

            serializer = CallsPlanSerializer(data=calls_plan_list, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if all_month:
            # обновление плана всех дней месяца
            entries = CallsPlan.objects.filter(
                calendar__date_calendar__year=year,
                calendar__date_calendar__month=month,
                employee__ID=employee
            ).update(count_calls=count_calls)
            return Response(True, status=status.HTTP_201_CREATED)
        else:
            # обновление плана за один день
            entry = CallsPlan.objects.filter(
                calendar__date_calendar__year=year,
                calendar__date_calendar__month=month,
                calendar__date_calendar__day=day,
                employee__ID=employee
            ).update(count_calls=count_calls)
            return Response(True, status=status.HTTP_201_CREATED)


# Изменение плана по звонкам - NEW
class CallsPlanCompletedViewSet(views.APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        calendar_date = request.data.get("calendar", None)  # дата: гггг-мм-дд
        employee = request.data.get("employee", None)  # ID работника
        plan_completed = request.data.get("plan_completed", None)  # план выполнен

        if not calendar_date:
            return Response('"calendar": обязательное поле', status=status.HTTP_400_BAD_REQUEST)

        if not employee:
            return Response('"employee": обязательное поле', status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.datetime.strptime(calendar_date, "%Y-%m-%d")
            year = date.year
            month = date.month
            day = date.day
        except ValueError:
            return Response('"calendar": не правильный формат даты, требуется формат "гггг-мм-дд"',
                            status=status.HTTP_400_BAD_REQUEST)

        entry = CallsPlan.objects.filter(
            calendar__date_calendar__year=year,
            calendar__date_calendar__month=month,
            calendar__date_calendar__day=day,
            employee__ID=employee
        ).update(plan_completed=plan_completed)

        if entry == 1:
            return Response(True, status=status.HTTP_201_CREATED)

        return Response(False, status=status.HTTP_201_CREATED)


# получение данных сгруппированных по месяцам одного года
class RationActiveByMonthApiView(views.APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        departs = request.data.get("depart", "1")
        year = request.data.get("year", 2021)
        duration = request.data.get("duration", 20)
        departments = departs.split(",")

        # получение списка пользователей
        users = common.get_users_by_depeartments(departments)

        # получение фактического количества звонков по месяцам
        calls = common.get_calls_by_month(departments, year, duration)

        # получение фактического количества встреч по месяцам
        meetings = common.get_meetings_by_month(departments, year)

        # получение списка комментариев
        comments = Comment.objects.select_related("recipient").only(
            "recipient__UF_DEPARTMENT",
            "recipient__ACTIVE",
            "recipient__STATUS_DISPLAY",
            "date_comment"
        ).filter(
            recipient__UF_DEPARTMENT__in=departments,
            recipient__ACTIVE=True,
            recipient__STATUS_DISPLAY=True,
            date_comment__year=year,
        ).values(
            'recipient__ID', 'date_comment__month'
        ).annotate(
            counts=models.Count('date_comment')
        )

        # получение плана по звонкам
        calls_plan = CallsPlan.objects.select_related("calendar").only(
            "calendar__date_calendar",
            'employee__ID',
            'count_calls_avg'
        ).filter(
            calendar__date_calendar__year=year,
        ).annotate(
            count_calls_avg=models.Avg("count_calls"),
            plan_completed_avg=models.Avg("plan_completed"),
        ).values(
            'employee__ID', 'count_calls_avg', 'calendar__date_calendar__month'
        )

        data = {}
        for department in departments:
            data[department] = []

        data_user = {}
        for user in users:
            user["calls_fact"] = {}
            user["meetings_fact"] = {}
            user["comments"] = {}
            user["calls_plan"] = {}
            key = user["ID"]
            data_user[key] = user

        for (user_id, month_num), count in calls.items():
            if user_id in data_user:
                data_user[user_id]["calls_fact"][month_num] = count

        for meeting in meetings:
            user = meeting["RESPONSIBLE_ID__ID"]
            month = meeting["END_TIME__month"]
            count = meeting["counts"]
            if user in data_user:
                data_user[user]["meetings_fact"][month] = count

        for comment in comments:
            user = comment["recipient__ID"]
            month = comment["date_comment__month"]
            count = comment["counts"]
            if user in data_user:
                data_user[user]["comments"][month] = count

        for plan in calls_plan:
            user = plan["employee__ID"]
            month = plan["calendar__date_calendar__month"]
            count = plan["count_calls_avg"]
            if user in data_user:
                data_user[user]["calls_plan"][month] = count

        for user_id, user in data_user.items():
            dep = str(user["UF_DEPARTMENT"])
            data[dep].append(user)

        return Response(data, status=status.HTTP_200_OK)


# получение данных сгруппированных по дням одного месяца
class RationActiveByDayApiView(views.APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        departs = request.data.get("depart", "1")
        year = request.data.get("year", 2021)
        month = request.data.get("month", 11)
        duration = request.data.get("duration", 20)
        departments = departs.split(",")

        # получение списка пользователей
        users = common.get_users_by_depeartments(departments)

        # получение фактического количества звонков по дням за месяц
        calls = common.get_calls_by_day(departments, year, month, duration)

        # получение фактического количества встреч по дням за месяц
        meetings = common.get_meetings_by_day(departments, year, month)

        # получение списка комментариев
        comments = Comment.objects.select_related("recipient").only(
            "recipient__UF_DEPARTMENT",
            "recipient__ACTIVE",
            "recipient__STATUS_DISPLAY",
            "date_comment"
        ).filter(
            recipient__UF_DEPARTMENT__in=departments,
            recipient__ACTIVE=True,
            recipient__STATUS_DISPLAY=True,
            date_comment__year=year,
            date_comment__month=month,
        ).values(
            'recipient__ID', 'date_comment__day'
        ).annotate(
            counts=models.Count('date_comment')
        )

        # получение плана по звонкам
        calls_plan = CallsPlan.objects.select_related("calendar").only(
            "calendar__date_calendar",
            'employee__ID',
            'count_calls_avg',
            'plan_completed'
        ).filter(
            calendar__date_calendar__year=year,
            calendar__date_calendar__month=month,
        ).values(
            'employee__ID', 'count_calls', 'plan_completed', 'calendar__date_calendar__day'
        )

        data = {}
        for department in departments:
            data[department] = []

        data_user = {}
        for user in users:
            user["calls_fact"] = {}
            user["meetings_fact"] = {}
            user["comments"] = {}
            user["calls_plan"] = {}
            user["completed_plan"] = {}
            key = user["ID"]
            data_user[key] = user

        for (user_id, day_num), count in calls.items():
            if user_id in data_user:
               data_user[user_id]["calls_fact"][day_num] = count

        for meeting in meetings:
            user = meeting["RESPONSIBLE_ID__ID"]
            day = meeting["END_TIME__day"]
            count = meeting["counts"]
            if user in data_user:
                data_user[user]["meetings_fact"][day] = count

        for comment in comments:
            user = comment["recipient__ID"]
            day = comment["date_comment__day"]
            count = comment["counts"]
            if user in data_user:
                data_user[user]["comments"][day] = count

        for plan in calls_plan:
            user = plan["employee__ID"]
            day = plan["calendar__date_calendar__day"]
            count = plan["count_calls"]
            completed = plan["plan_completed"]
            if user in data_user:
                data_user[user]["calls_plan"][day] = count
                data_user[user]["completed_plan"][day] = completed

        for user_id, user in data_user.items():
            dep = str(user["UF_DEPARTMENT"])
            data[dep].append(user)

        return Response(data, status=status.HTTP_200_OK)

