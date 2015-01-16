from django.core.management.base import BaseCommand, CommandError
from abon.models import Bill, Abonent
from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = datetime.now()
        count = 0
        total = Abonent.objects.all().count()
        for a in Abonent.objects.all():
            elapsed = (datetime.now() - start)
            done = float("%0.4f" % (count / total))
            eta = timedelta(seconds=(elapsed.seconds/done))
            a.fix_bill_history()
            count += 1
            if not (count % 20):
                print "%s/%s %s%% elapsed: %s remaining: %s" % (count, total, done*100, str(elapsed), str(eta))
