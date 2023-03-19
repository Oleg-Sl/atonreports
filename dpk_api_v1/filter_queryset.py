from django_filters import rest_framework as filters


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


class CompanyIdFilter(filters.RangeFilter, filters.DateFilter):
    pass


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class StatisticCompany(filters.FilterSet):
    company = NumberInFilter(field_name='ID', lookup_expr='in')
    responsible = NumberInFilter(field_name='ASSIGNED_BY_ID__ID', lookup_expr='in')

    sector = filters.CharFilter(lookup_expr="icontains")
    region = filters.CharFilter()
    source = filters.CharFilter()
    requisite_region = filters.CharFilter()
    requisites_city = filters.CharFilter()

    number_employees = filters.RangeFilter()
    REVENUE = filters.RangeFilter()
    DATE_CREATE = filters.DateFromToRangeFilter()

    # inn = filters.CharFilter(field_name='inn', lookup_expr="regex")
    inn = filters.CharFilter(lookup_expr="regex")
    # inn = filters.CharFilter()

    class Meta:
        model = Company
        fields = ["company", "ASSIGNED_BY_ID", "sector", "region", "source",
                  "requisite_region", "requisites_city", "number_employees",
                  "REVENUE", "DATE_CREATE", "inn", ]


class StatisticCompanyByDirection(filters.FilterSet):
    company = NumberInFilter(field_name='ID', lookup_expr='in')

    class Meta:
        model = Company
        fields = ["company", ]


class StatisticByDirection(filters.FilterSet):
    direction = NumberInFilter(field_name='ID', lookup_expr='in')

    class Meta:
        model = Direction
        fields = ["direction", ]
