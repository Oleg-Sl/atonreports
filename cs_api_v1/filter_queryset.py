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
    CALL_START_DATE = filters.DateFromToRangeFilter(field_name='CALL_START_DATE')
    DURATION = filters.NumberFilter(field_name='DURATION', lookup_expr='gte')
    # RESPONSIBLE_ID = filters.NumberFilter(field_name='RESPONSIBLE_ID__ID', lookup_expr='eq')

    class Meta:
        model = Activity
        fields = ["RESPONSIBLE_ID__ID", "CREATED", "DURATION", "CALL_START_DATE"]


class CommentFilter(filters.FilterSet):
    date_comment = filters.DateFromToRangeFilter()
    # recipient = filters.NumberFilter(field_name='recipient__ID', lookup_expr='eq')
    # commentator = filters.NumberFilter(field_name='commentator__ID', lookup_expr='eq')

    class Meta:
        model = Comment
        fields = ["recipient__ID", "commentator__ID", "date_comment", ]
