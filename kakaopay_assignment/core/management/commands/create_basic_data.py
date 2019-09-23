from django.core.management.base import BaseCommand
from stats.models import Stat
from devices.models import Device


class Command(BaseCommand):
    help = 'Create 6 meeting rooms for test'

    def handle(self, *args, **options):
        Stat.load_initial_data()
        Device.load_initial_data()
        self.stdout.write(self.style.SUCCESS('Successfully created basic data'))
