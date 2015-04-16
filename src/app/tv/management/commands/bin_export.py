# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from django.core.management.base import BaseCommand, CommandError
from scrambler.scrambler import UserExport, ChannelExport
from django.conf import settings
import subprocess

settings.DEBUG = False
HOST = "192.168.33.152"
USER = "maxim"
REMOTE_DIR = "~/scrambler"
PROG_BIN = "%s/prog.bin" % settings.EXPORT_PATH
USER_BIN = "%s/user.bin" % settings.EXPORT_PATH
SCR_IP = "192.168.17.41"

SSH_AUTH = "{user}@{host}".format(user=USER, host=HOST)
SCP_PATH = "{user}@{host}:{dir}".format(user=USER, host=HOST, dir=REMOTE_DIR)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print "bin export begin"
        settings.DEBUG = False
        ChannelExport.export()
        print "prog.bin ready"
        UserExport.export()
        print "user.bin ready"
        subprocess.call(["scp", USER_BIN, SCP_PATH])
        subprocess.call(["scp", PROG_BIN, SCP_PATH])
        subprocess.call(["ssh", SSH_AUTH, "scrambler/scr1fs", "192.168.17.41", '"prog.bin"', '"user.bin"'])
        print "export done"