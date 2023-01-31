import pprint
from django.core.management.base import BaseCommand

from dataapp.services.tasks import creat_deals


class Command(BaseCommand):
    help = 'Save deals to DB'

    def handle(self, *args, **kwargs):
        creat_deals.create_or_update_deals()
