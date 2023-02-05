from rest_framework import serializers
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


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class SectorCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['sector']


class RegionCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['region']


class SourceCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['source']


class RequisitesRegionCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['requisite_region']


class RequisitesCityCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['requisites_city']


class StatisticCompanySerializer(serializers.ModelSerializer):
    summa_by_company_success = serializers.FloatField()
    summa_by_company_work = serializers.FloatField()
    date_last_communication = serializers.DateTimeField()

    class Meta:
        model = Company
        fields = ("ID", "TITLE", "ASSIGNED_BY_ID", "date_last_communication", "summa_by_company_success", "summa_by_company_work")
        # fields = '__all__'





def converting_list_to_dict(queryset, key_depth_first=None, key_depth_second=None):
    response = {}
    for element in queryset:
        if not response.get(element[key_depth_first]):
            response[element[key_depth_first]] = {}

        if key_depth_second:
            response[element[key_depth_first]][element[key_depth_second]] = element
        else:
            response[element[key_depth_first]] = element

    return response






