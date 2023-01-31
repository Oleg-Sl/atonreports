import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone


from dataapp.services.tasks import creat_activities


class Command(BaseCommand):
    help = 'Save activities to DB'

    def handle(self, *args, **kwargs):
        creat_activities.creat_and_update_activities()