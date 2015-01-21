from django.core.management.base import BaseCommand, CommandError
from abon.models import Bill, Abonent
from datetime import datetime, timedelta
from optparse import make_option
import gc


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    d["hours"] = str(d["hours"]).zfill(2)
    d["minutes"] = str(d["minutes"]).zfill(2)
    d["seconds"] = str(d["seconds"]).zfill(2)
    return fmt.format(**d)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "-s",
            "--skip",
            dest="skip",
            help="skip abonents from beginning",
            metavar="SKIP"
        ),
    )

    def handle(self, *args, **options):
        gc.disable()
        start = datetime.now()
        count = 0
        abonlist = Abonent.objects.all()
        if int(options['skip'] or 0)>0:
            abonlist = abonlist[int(options['skip']):]
        total = abonlist.count()
        for a in abonlist:
            count += 1
            a.fix_bill_history()
            if not (count % 20):
                elapsed = (datetime.now() - start)
                done = float("%0.4f" % (float(count) / float(total)))
                if done>0:
                    eta = timedelta(seconds=(elapsed.seconds/done))
                else:
                    eta = timedelta(seconds=0)
                print "%6s of %6s done %5s%%. elapsed: %s remaining: %s" % (
                    count, total, "%0.2f" % (done*100),
                    strfdelta(elapsed, "{hours}:{minutes}:{seconds}"),
                    strfdelta(elapsed-eta, "{hours}:{minutes}:{seconds}")
                )
            if not (count % 100):
                gc.collect()
