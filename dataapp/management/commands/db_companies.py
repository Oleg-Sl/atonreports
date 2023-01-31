import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone


from dataapp.services.tasks import creat_companies


class Command(BaseCommand):
    help = 'Save companies to DB'

    def handle(self, *args, **kwargs):
        creat_companies.create_or_update_companies()
