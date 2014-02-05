from django.core.management.base import BaseCommand, CommandError
from tv.models import TariffPlan
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        source = TariffPlan.objects.get(pk=settings.CHAN_COPY_SOURCE)
        for tp in TariffPlan.objects.filter(pk__in=settings.CHAN_COPY_DESTINATION):
            tp.copy_channels(source)
