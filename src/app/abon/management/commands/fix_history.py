from django.core.management.base import BaseCommand, CommandError
from abon.models import Bill, Abonent


class Command(BaseCommand):

    def handle(self, *args, **options):
        count = 0
        total = Abonent.objects.all().count()
        for a in Abonent.objects.all():
            a.fix_bill_history()
            count += 1
            if not (count % 20):
                print "%s/%s" % (count, total)
