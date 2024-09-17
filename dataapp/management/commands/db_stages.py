from django.core.management.base import BaseCommand

from dataapp.services.tasks import creat_stages


class Command(BaseCommand):
    help = 'Save stages to DB'

    def handle(self, *args, **kwargs):
        creat_stages.create_or_update_stages()
