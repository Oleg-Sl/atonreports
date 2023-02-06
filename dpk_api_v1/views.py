from rest_framework import views, viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from datetime import datetime, timedelta, timezone, date
import logging

# from .services.bitrix24 import verification_app, tokens
# from .services.converter import converting_list_to_dict
# from .services.filter_queryset import statistic_company
from . import filter_queryset


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
    DirectionSerializer,
    StageSerializer,
    CompanySerializer,
    SectorCompanySerializer,
    RegionCompanySerializer,
    SourceCompanySerializer,
    RequisitesRegionCompanySerializer,
    RequisitesCityCompanySerializer,
    StatisticCompanySerializer,
    # CompanyOpportunitySerializer,
    converting_list_to_dict,
)



class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'install': reverse('dpk_api_v1:install', request=request, format=format),
        'uninstall': reverse('dpk_api_v1:uninstall', request=request, format=format),
        'index': reverse('dpk_api_v1:index', request=request, format=format),

        'directions': reverse('dpk_api_v1:directions-list', request=request, format=format),
        'stages': reverse('dpk_api_v1:stages-list', request=request, format=format),
        'companies': reverse('dpk_api_v1:companies-list', request=request, format=format),
        'region_companies': reverse('dpk_api_v1:region_companies-list', request=request, format=format),
        'sector_companies': reverse('dpk_api_v1:sector_companies-list', request=request, format=format),
        'source_companies': reverse('dpk_api_v1:source_companies-list', request=request, format=format),
        'requisite_region': reverse('dpk_api_v1:requisite_region-list', request=request, format=format),
        'requisites_city': reverse('dpk_api_v1:requisites_city-list', request=request, format=format),

        'statistic-company': reverse('dpk_api_v1:statistic-company-list', request=request, format=format),
        'statistic-company-new': reverse('dpk_api_v1:statistic-company-new-list', request=request, format=format),
        'statistic-direction': reverse('dpk_api_v1:statistic-direction-list', request=request, format=format),
        'statistic-company-direction': reverse('dpk_api_v1:statistic-company-direction-list', request=request, format=format),

        'create-update-direction': reverse('dpk_api_v1:create_update_direction', request=request, format=format),
        'create-update-stages': reverse('dpk_api_v1:create_update_stages', request=request, format=format),
        'create-update-company': reverse('dpk_api_v1:create_update_company', request=request, format=format),
        'create-update-deal': reverse('dpk_api_v1:create_update_deal', request=request, format=format),
        'create-update-calls': reverse('dpk_api_v1:create_update_calls', request=request, format=format),
    })


class InstallAppApiView(views.APIView):
    permission_classes = [AllowAny]

    @xframe_options_exempt
    def post(self, request):
        return render(request, 'dpk/install.html')


class UninstallAppApiView(views.APIView):
    permission_classes = [AllowAny]

    @xframe_options_exempt
    def post(self, request):
        return Response(status.HTTP_200_OK)


class IndexApiView(views.APIView):
    permission_classes = [AllowAny]

    @xframe_options_exempt
    def post(self, request):
        return render(request, 'dpk/index.html', context={
            "DOMAIN": "https://otchet.atonlab.ru/reports/"
        })

    @xframe_options_exempt
    def get(self, request):
        return render(request, 'dpk/index.html')


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.filter(new=True)
    serializer_class = DirectionSerializer
    http_method_names = ['get', 'options']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    http_method_names = ['get', 'options']
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^ID", "TITLE", "^inn"]
    http_method_names = ['get', 'options']
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


class SectorCompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(sector__isnull=False).values("sector").distinct("sector")
    serializer_class = SectorCompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^sector", ]
    http_method_names = ['get', 'options']
    permission_classes = [IsAuthenticated]


class RegionCompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(region__isnull=False).values("region").distinct("region")
    serializer_class = RegionCompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^region", ]
    http_method_names = ['get', 'options']
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


class SourceCompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(source__isnull=False).values("source").distinct("source")
    serializer_class = SourceCompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^source", ]
    http_method_names = ['get', 'options']
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


class RequisitesRegionCompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(requisite_region__isnull=False).values("requisite_region").distinct("requisite_region")
    serializer_class = RequisitesRegionCompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^requisite_region", ]
    http_method_names = ['get', 'options']
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


class RequisitesCityCompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(requisites_city__isnull=False).values("requisites_city").distinct("requisites_city")
    serializer_class = RequisitesCityCompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^requisites_city", ]
    http_method_names = ['get', 'options']
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]


class StatisticCompanyViewSet(viewsets.GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = StatisticCompanySerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = filter_queryset.StatisticCompany
    ordering_fields = ["ID", "TITLE", "ASSIGNED_BY_ID", "date_last_communication", "summa_by_company_success", "summa_by_company_work"]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    # def get_queryset(self):
    #     duration = self.request.query_params.get("duration", "0")
    #     return super().get_queryset().statistic_company(duration)

    # def list(self, request, *args, **kwargs):
    #     duration = request.query_params.get("duration", "0")
    #     if not duration.isdigit():
    #         return Response('The "duration" value must be an integer', status=status.HTTP_400_BAD_REQUEST)
    #
    #     queryset = self.filter_queryset(
    #         self.get_queryset()
    #     )
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #
    #     return Response(serializer.data)


class StatisticCompanyDirectionViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def get_queryset(self, companies_ids, directions_ids, limit_date_suspended_deals, limit_date_failed_deals):
        return Deal.objects.statistic_company_by_directions(
            companies_ids,
            directions_ids,
            limit_date_suspended_deals,
            limit_date_failed_deals
        )

    def list(self, request, *args, **kwargs):
        companies_str = request.query_params .get("companies", "")
        directions_str = request.query_params.get("directions", "")
        days_for_suspended_deals_str = request.query_params.get("days_for_suspended_deals", settings.DEFAULT_DELTA_DEYS_SUSPENDED_DEALS)
        days_for_failed_deals_str = request.query_params.get("days_for_failed_deals", settings.DEFAULT_DELTA_DEYS_FAILED_DEALS)
        # ID компаний
        companies_ids = [int(el) for el in companies_str.split(",") if isinstance(el, str) and el.isdigit()]
        # ID направлений
        directions_ids = [int(el) for el in directions_str.split(",") if isinstance(el, str) and el.isdigit()]

        if not days_for_suspended_deals_str.isdigit() or not days_for_failed_deals_str.isdigit():
            return Response(
                'The "days_for_suspended_deals" and "days_for_failed_deals" variables must be a number',
                status=status.HTTP_400_BAD_REQUEST
            )

        limit_date_suspended_deals = datetime.now(timezone.utc) - timedelta(days=int(days_for_suspended_deals_str))
        limit_date_failed_deals = datetime.now(timezone.utc) - timedelta(days=int(days_for_failed_deals_str))

        queryset = self.filter_queryset(
            self.get_queryset(companies_ids, directions_ids, limit_date_suspended_deals, limit_date_failed_deals)
        )

        # response = queryset
        response = converting_list_to_dict(queryset, "company__ID", "direction__ID")
        return Response(response, status=status.HTTP_200_OK)


class StatisticDirectionViewSet(viewsets.GenericViewSet):
    queryset = Direction.direction_actual.count_active_deals()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = filter_queryset.StatisticByDirection
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = converting_list_to_dict(queryset, "ID")
        return Response(response, status=status.HTTP_200_OK)


class StatisticCompanyOpportunityViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def get_queryset(self, companies_ids):
        return Company.statistic.statistic_company_summary(companies_ids)

    def list(self, request, *args, **kwargs):
        companies_str = request.query_params.get("companies", "")
        companies_ids = [int(el) for el in companies_str.split(",") if isinstance(el, str) and el.isdigit()]
        queryset = self.filter_queryset(self.get_queryset(companies_ids))
        # response = converting_list_to_dict(queryset, "company__ID")
        # return Response(response, status=status.HTTP_200_OK)
        return Response(queryset, status=status.HTTP_200_OK)
