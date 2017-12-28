from django.core.management.base import BaseCommand
from django.db.models import Count
from datetime import datetime

from tv.models import Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        dt = datetime(2017, 12, 27)
        payments = Payment.objects.filter(timestamp__gte=dt).values('bill', 'sum').annotate(count=Count('bill')).filter(
            count__gt=1).order_by('bill')
        print(payments.count())

        for p in payments:
            dups = Payment.objects.filter(timestamp__gte=dt, bill=p['bill'])
            if dups.count() > 1:
                print dups[1]
                dups[1].rollback()

