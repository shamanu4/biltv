# -*- encoding: utf-8 -*-
__author__ = 'maxim'

import signal
import time

import tornado.httpserver
import tornado.ioloop

from django.core.management.base import BaseCommand, CommandError

from ui.tornado_main import application
from django.conf import settings
from tv.models import CardService


class Command(BaseCommand):

    def handle(self, *args, **options):
        css = CardService.objects.filter(extra__isnull=False)
        for cs in css:
            for link in cs.abills_links.all():
                link.sync()

