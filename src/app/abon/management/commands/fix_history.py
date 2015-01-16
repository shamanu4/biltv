from django.core.management.base import BaseCommand, CommandError
from abon.models import Bill, Abonent
from datetime import datetime, timedelta
from optparse import make_option
import gc


class Command(BaseCommand):
    args = '<skip>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        gc.enable()
        gc.set_debug(gc.DEBUG_STATS)
        option_list = BaseCommand.option_list + (
            make_option(
                "-s",
                "--skip",
                dest="skip",
                help="skip abonents from beginning",
                metavar="SKIP"
            ),
        )

        start = datetime.now()
        count = 0
        abonlist = Abonent.objects.all()
        if int(options['skip'])>0:
            abonlist = abonlist[int(options['skip']):]
        total = abonlist.count()
        for a in abonlist:
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
            if not (count % 20):
                print "garbage collecting ..."
                gc.collect()
                print "done"
