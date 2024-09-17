from django.core.management.base import BaseCommand

from dataapp.services.tasks import creat_directions


class Command(BaseCommand):
    help = 'Save directions to DB'

    def handle(self, *args, **kwargs):
        creat_directions.create_or_update_directions()
