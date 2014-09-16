from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from statements.models import Statement, Entry
import pandas as pd
import os
from datetime import datetime
from unidecode import unidecode
import json
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


class Command(BaseCommand):
    help = 'Parse xls file from PB'

    args = '<path, date>'

    option_list = BaseCommand.option_list + (
        make_option('--process',
                    action='store_true',
                    dest='process',
                    default=False,
                    help='Save data instead of returning it'),
    )

    def handle(self, *args, **options):
        try:
            path = args[0]
        except IndexError:
            raise CommandError("Required argument [0]: path")
        date = None
        if options['process']:
            try:
                date = args[1]
            except IndexError:
                raise CommandError("Required argument [1]: date")
        if not os.path.exists(path):
            raise CommandError("Path [%s] does not exist" % path)
        else:
            try:
                parsed = pd.read_html(path, infer_types=False)
            except Exception, e:
                raise CommandError("Can't parse file. Error: %s" % e)
            else:
                # @TODO: find proper head and data structures in file.
                head = parsed[2]
                data = parsed[3]
            statement = {
                'day': date,
                'opcount': int(float(head[1][2])),
                'remains': float("%0.2f" % float(head[1][0])),
                'turnover': float("%0.2f" % float(head[1][1])),
            }
            entries = []
            for i in xrange(1, statement['opcount']+1):
                dt = datetime.strptime(str(data[1][i]), "%d.%m.%Y").date()
                tm = datetime.strptime(str(data[2][i]), "%H:%M:%S").time()
                pid = str(data[0][i])
                timestamp = datetime.combine(dt, tm).strftime("%Y-%m-%d %H:%M:%S")
                amount = float("%0.2f" % float(data[3][i]))
                currency = str(data[4][i])
                egrpou = str(data[5][i])
                verbose_name = unicode(data[6][i])
                account_num = str(data[7][i])
                mfo = str(data[8][i])
                descr = unicode(data[9][i])
                e = {
                    'pid': pid,
                    'timestamp': timestamp,
                    'amount': amount,
                    'currency': currency,
                    'egrpou': egrpou,
                    'verbose_name': verbose_name,
                    'account_num': account_num,
                    'mfo': mfo,
                    'descr': descr
                }
                entries.append(e)

            if not options['process']:
                return json.dumps({
                    'statement': statement,
                    'entries': entries
                })
            try:
                s = Statement.objects.create(**statement)
                for e in entries:
                    Entry.objects.create(statement=s, **e)
                s.save()
            except Exception, e:
                raise CommandError("Database consistency error")