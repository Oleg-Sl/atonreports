import pprint
from django.core.management.base import BaseCommand

from dataapp.services.tasks import creat_users


class Command(BaseCommand):
    help = 'Save users to DB'

    def handle(self, *args, **kwargs):
        creat_users.create_or_update_users()
