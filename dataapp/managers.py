import datetime
from django.db import models
from django.conf import settings


class CompanyQuerySet(models.QuerySet):
    def statistic_company(self, duration):
        return self.annotate(dpk=models.functions.Coalesce(
            models.Max("activity__CALL_START_DATE", filter=models.Q(activity__DURATION__gte=duration)),
            datetime.date(2000, 1, 1)
        ))


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(ID=0)


class DirectionActualManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(ID__in=settings.DIRECTION_IGNORE_LIST).filter(new=True)

    def count_active_deals(self):
        return self.annotate(
            count_active_deal=models.Count(
                "deal",
                filter=models.Q(deal__CLOSED=False)
            )
        ).values('count_active_deal', 'ID', 'VALUE')
            # .values('count_active_deal', 'id_bx')
            # annotate(direction=models.F("id_bx"))


class DealManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().exclude(direction__pk__in=settings.DIRECTION_IGNORE_LIST)

    def statistic_company_by_directions(self, companies, directions, lim_date_suspended_deals, lim_date_failed_deals):
        from .models import Deal, Company
        return self.filter(
            active=True,
            company__ID__in=companies,
        ).values(
            "company__ID", "direction__ID"
        ).annotate(
            name=models.F("direction__VALUE"),
            # дата последнего изменения сделки
            date_last_modify=models.Max("DATE_MODIFY"),
            # кол-во сделок в работе
            count_deals_in_work=models.Count("pk", filter=models.Q(CLOSED=False)),
            # есть не просроченные сделки в работе
            actual_deal_work=models.ExpressionWrapper(
                models.Q(stage__status="WORK") & models.Q(DATE_MODIFY__gte=lim_date_suspended_deals),
                output_field=models.BooleanField()
            ),
            # есть не просроченные сделки на подготовке к работе
            actual_deal_preparation=models.ExpressionWrapper(
                models.Q(stage__status="PREPARATION") & models.Q(DATE_MODIFY__gte=lim_date_suspended_deals),
                output_field=models.BooleanField()
            ),
            # есть не просроченные провальные сделки
            actual_deal_failed=models.ExpressionWrapper(
                models.Q(stage__status="FAILURE") & models.Q(DATE_MODIFY__gte=lim_date_failed_deals),
                output_field=models.BooleanField()
            ),
            # сумма стоимостей успешных сделок
            # opportunity_success=models.Sum("opportunity", filter=models.Q(stage__status="SUCCESSFUL")),
            opportunity_success=models.Subquery(
                    Company.statistic.filter(
                        ID=models.OuterRef('company__ID'),
                        deal__direction__ID=models.OuterRef('direction__ID'),
                        deal__stage__status="WON"
                    ).annotate(
                        s=models.Sum('deal__opportunity')
                    ).values('s')[:1]
                ),
            # сумма стоимостей сделок в работе
            opportunity_work=models.Subquery(
                    Company.statistic.filter(
                        ID=models.OuterRef('company__ID'),
                        deal__direction__ID=models.OuterRef('direction__ID'),
                        deal__stage__status="WORK"
                    ).annotate(
                        s=models.Sum('deal__opportunity')
                    ).values('s')[:1]
                ),
        )

    def statistic_company_summary(self, companies):
        from .models import Deal
        return self.filter(
            company__ID__in=companies,
        ).values(
            "company__ID"
        ).annotate(
            summa_by_company_success=models.Sum("opportunity", filter=models.Q(direction__new=True, stage__status="WON")),
            # summa_by_company_success=models.Subquery(
            #     Deal.objects.filter(
            #         company=models.OuterRef('company__pk'),
            #         direction__new=True,
            #         stage__status="SUCCESSFUL"
            #     ).annotate(
            #         s=models.Sum('opportunity')
            #     ).values('s')[:1]
            # ),
            summa_by_company_work=models.Subquery(
                Deal.objects.filter(
                    company__ID=models.OuterRef('company__ID'),
                    direction__new=True,
                    stage__status="WORK"
                ).annotate(
                    s=models.Sum('opportunity')
                ).values('s')[:1]
            ),
        )


class CompanyStatisticManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(ID=0)

    def statistic_company_by_directions(self, companies, lim_date_suspended_deals, lim_date_failed_deals):
        from .models import Deal
        return self.filter(
            pk__in=companies,
            # active=True
        ).values(
            "pk", "deal__direction"
        ).annotate(
            name=models.F("deal__direction__VALUE"),
            # дата последнего изменения сделки
            date_last_modify=models.Max("deal__DATE_MODIFY"),
            # кол-во сделок в работе
            count_deals_in_work=models.Count("deal", filter=models.Q(CLOSEDATE=False)),
            # есть не просроченные сделки в работе
            actual_deal_work=models.ExpressionWrapper(
                models.Q(deal__stage__status="WORK") & models.Q(deal__DATE_MODIFY__gte=lim_date_suspended_deals),
                output_field=models.BooleanField()
            ),
            # есть не просроченные сделки на подготовке к работе
            actual_deal_preparation=models.ExpressionWrapper(
                models.Q(deal__stage__status="PREPARATION") & models.Q(deal__DATE_MODIFY__gte=lim_date_suspended_deals),
                output_field=models.BooleanField()
            ),
            # есть не просроченные провальные сделки
            actual_deal_failed=models.ExpressionWrapper(
                models.Q(deal__stage__status="FAILURE") & models.Q(deal__DATE_MODIFY__gte=lim_date_failed_deals),
                output_field=models.BooleanField()
            ),
            # сумма стоимостей успешных сделок
            opportunity_success=models.Sum("deal__opportunity", filter=models.Q(deal__stage__status="WON")),
            # сумма стоимостей сделок в работе
            # opportunity_work=models.Sum("opportunity", filter=models.Q(stage__status="WORK")),
            opportunity_work=models.Subquery(
                    Deal.objects.filter(
                        company=models.OuterRef('pk'),
                        direction=models.OuterRef('deal__direction__pk'),
                        stage__status="WORK"
                    ).annotate(
                        s=models.Sum('opportunity')
                    ).values('s')[:1]
                ),
            summa_by_company_success=models.Subquery(
                Deal.objects.filter(
                    company=models.OuterRef('pk'),
                    direction__new=True
                    # stage__status="SUCCESSFUL"
                ).annotate(
                    s=models.Sum('opportunity')
                ).values('s')[:1]
            ),
            summa_by_company_work=models.Subquery(
                Deal.objects.filter(
                    company=models.OuterRef('pk'),
                    direction__new=True
                    # stage__status="WORK"
                ).annotate(
                    s=models.Sum('opportunity')
                ).values('s')[:1]
            ),
        )

    def statistic_company_summary(self, companies):
        from .models import Deal, Company
        return self.filter(
            pk__in=companies,
        ).annotate(
            summa_by_company_success1=models.Subquery(
                Company.statistic.filter(
                    pk=models.OuterRef('pk'),
                    deal__direction__new=True,
                    deal__stage__status="WON"
                ).annotate(
                    s=models.Sum('deal__opportunity')
                ).values('s')[:1]
            ),
            summa_by_company_work1=models.Subquery(
                Company.statistic.filter(
                    pk=models.OuterRef('pk'),
                    deal__direction__new=True,
                    deal__stage__status="WORK"
                ).annotate(
                    s=models.Sum('deal__opportunity')
                ).values('s')[:1]
            ),
        ).values(
            "pk", "summa_by_company_success1", "summa_by_company_work1"
        )

