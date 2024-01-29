from django.core.management.base import BaseCommand
import csv
import datetime
from django.db import models
from django.db.models import Sum, Count, F
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


class Command(BaseCommand):
    help = 'Save data to csv file'

    def handle(self, *args, **kwargs):
        queriset = Company.objects.filter(active=True, ID=146).prefetch_related('deal__direction').values(
        'ID', 'TITLE', 'sector', 'region', 'requisite_region', 'number_employees', 'REVENUE', 'inn', 'deal__direction__VALUE'
        ).annotate(
            date_last_modify=models.Max("deal__DATE_MODIFY"),
            count_deals_in_work=models.Count("pk", filter=models.Q(deal__CLOSED=False)),
            count_deals_success=models.Count("pk", filter=models.Q(deal__CLOSED=True)),
            opportunity_success=models.Subquery(
                            Company.statistic.filter(
                                ID=models.OuterRef('ID'),
                                deal__direction__ID=models.OuterRef('deal__direction__ID'),
                                deal__stage__status="WON"
                            ).annotate(
                                s=models.Sum('deal__opportunity')
                            ).values('s')[:1]
                        ),
            opportunity_work=models.Subquery(
                Company.statistic.filter(
                ID=models.OuterRef('ID'),
                deal__direction__ID=models.OuterRef('deal__direction__ID'),
                deal__stage__status="WORK"
                ).annotate(
                s=models.Sum('deal__opportunity')
                ).values('s')[:1]
            ),
        )

        csv_file_path = self.generate_filename()
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'ID', 'TITLE', 'sector', 'region', 'requisite_region', 'number_employees', 'REVENUE', 'inn',
                'deal__direction__VALUE', 'date_last_modify', 'count_deals_in_work', 'count_deals_success',
                'opportunity_success', 'opportunity_work'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for row in queriset:
                writer.writerow(row)

    def generate_filename(self):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"output_data_{formatted_date}.csv"
        return filename
