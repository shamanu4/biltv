from django.core.management.base import BaseCommand, CommandError
from abon.models import Bill

class Command(BaseCommand):

    def handle(self, *args, **options):
        count = 0
        total = Bill.objects.all().count()
        for bill in Bill.objects.all():
            bill.balance2set()
            count += 1
            if not (count % 20):
                print "%s/%s" % (count, total)
