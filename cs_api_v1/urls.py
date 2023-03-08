from django.urls import include, path
from rest_framework import routers
from django.views.decorators.cache import cache_page
from django.conf import settings


from .views import (
    InstallApiView,
    IndexApiView,
    UsersViewSet,
    CallsViewSet,
    CommentViewSet,
    ProductionCalendarViewSet,
    CallsPlanViewSet,
    CallsPlanCompletedViewSet,
    RationActiveByMonthApiView,
    RationActiveByDayApiView,
    CountsCompanyToCallsByMonthApiView,
    CountsCompanyToCallsSummaryApiView,
)


app_name = 'cs_api_v1'


router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'calls', CallsViewSet)
router.register(r'comment', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('install/', InstallApiView.as_view()),                         # вызывается при установке приложения
    path('index/', IndexApiView.as_view()),                             # вызывается при открытии приложения
    # path('app-uninstall/', AppUnistallApiView.as_view()),               # вызывается при удалении приложения

    # Добавление и изменение производственного календаря
    # Метод: GET. Параметры: year - год, status - (week/work) тип дня
    # Метод: POST. Данные: date_calendar - календарная дата, status - (week/work) тип дня
    path('production-calendar/', ProductionCalendarViewSet.as_view()),

    # Добавление и изменение плана по звонкам
    # Метод: GET. Параметры: year - год
    # Метод: POST. Данные: calendar - дата: гггг-мм-дд, employee - ID работника, count_calls - количество звонков, all_month - обновить план на весь месяц или один день
    path('calls-plan/', CallsPlanViewSet.as_view()),


    path('plan-completed/', CallsPlanCompletedViewSet.as_view()),


    # Получение данных статистики за год сгруппированные по месяцам
    # Метод: POST
    # Данные: depart - id подразделения, year - год, duration - минимальная длительность для учета в статистике
    path('active-by-month/', RationActiveByMonthApiView.as_view()),

    # Получение данных статистики за месяц сгруппированные по дням
    # Метод: POST
    # Данные: depart - id подразделения, year - год, month - нмер месяца, duration - миним. длит. для учета в статистике
    path('active-by-day/', RationActiveByDayApiView.as_view()),

    # Получение количества компаний в которые совершили звонки за год сгруппированные по месяцам
    # Метод: POST
    # Данные: depart - id подразделения, year - год
    path('company-calls-by-month/', CountsCompanyToCallsByMonthApiView.as_view()),

    path('company-calls-summary/', CountsCompanyToCallsSummaryApiView.as_view()),

]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += [path('index/__debug__/', include(debug_toolbar.urls))]


urlpatterns += router.urls



