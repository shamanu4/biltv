from django.core.management.base import BaseCommand, CommandError
from abon.models import Bill, Abonent
from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = datetime.now()
        count = 0
        total = Abonent.objects.all().count()
        for a in Abonent.objects.all():
            count += 1
            if not (count % 20):
                elapsed = (datetime.now() - start)
                done = float("%0.4f" % (float(count) / float(total)))
                if done>0:
                    eta = timedelta(seconds=(elapsed.seconds/done))
                else:
                    eta = "--:--:--"
                a.fix_bill_history()
                print "%s/%s %s%% elapsed: %s remaining: %s" % (count, total, done*100, str(elapsed), str(eta))
