from datetime import datetime, timedelta
from optparse import make_option

from django.core.management.base import BaseCommand
from abon.models import Abonent

from django.conf import settings
settings.DEBUG = False


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
            type="int",
            metavar="SKIP"
        ),
        make_option(
            "-d",
            "--dry-run",
            dest="dryrun",
            action="store_true",
            help="do not make any changes - only report them",
            metavar="DRYRUN"
        ),
        make_option(
            "-q",
            "--quiet",
            dest="quiet",
            action="store_true",
            help="do not display progress",
            metavar="QUIET"
        ),
    )

    def handle(self, *args, **options):
        start = datetime.now()
        count = initial = 0
        abonlist = Abonent.objects.all()
        if int(options['skip'] or 0) > 0:
            count = initial = int(options['skip'])
            abonlist = abonlist[count:]
        total = abonlist.count() + count
        for a in abonlist:
            count += 1
            a.fix_bill_history(dryrun=options['dryrun'])
            if not (count % 100) and not options['quiet']:
                elapsed = (datetime.now() - start)
                done = float("%0.4f" % (float(count - initial) / float(total - initial)))
                if done > 0:
                    eta = timedelta(seconds=(elapsed.seconds / done))
                else:
                    eta = timedelta(seconds=0)
                print "%6s of %6s done %5s%%. elapsed: %s remaining: %s" % (
                    count, total, "%0.2f" % (done * 100),
                    strfdelta(elapsed, "{hours}:{minutes}:{seconds}"),
                    strfdelta(eta - elapsed, "{hours}:{minutes}:{seconds}")
                )
            # if not (count % 100):
            # gc.collect()
