import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone


from dataapp.services.tasks import creat_calls


class Command(BaseCommand):
    help = 'Save calls to DB'

    def handle(self, *args, **kwargs):
        creat_calls.create_or_update_calls()
