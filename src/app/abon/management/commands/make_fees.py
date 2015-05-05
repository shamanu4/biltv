from django.core.management.base import BaseCommand, CommandError
from tv.models import FeesCalendar
from datetime import date
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        settings.DEBUG = False
        FeesCalendar.push_next_fee(date.today())