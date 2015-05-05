from django.core.management.base import BaseCommand, CommandError
from tv.models import FeesCalendar
from datetime import date


class Command(BaseCommand):

    def handle(self, *args, **options):
        from django.conf import settings
        settings.DEBUG = False
        FeesCalendar.push_next_fee(date.today())