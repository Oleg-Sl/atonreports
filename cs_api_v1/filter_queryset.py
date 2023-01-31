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


class CallsFilter(filters.FilterSet):
    CREATED = filters.DateFromToRangeFilter()
    CALL_START_DATE = filters.DateFromToRangeFilter(field_name='phone__CALL_START_DATE')
    CALL_DURATION = filters.NumberFilter(field_name='phone__CALL_DURATION', lookup_expr='gte')

    class Meta:
        model = Activity
        fields = ["RESPONSIBLE_ID", "CREATED", "CALL_DURATION", "CALL_START_DATE"]


class CommentFilter(filters.FilterSet):
    date_comment = filters.DateFromToRangeFilter()

    class Meta:
        model = Comment
        fields = ["recipient", "commentator", "date_comment", ]

