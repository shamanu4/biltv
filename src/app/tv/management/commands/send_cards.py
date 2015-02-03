# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from django.core.management.base import BaseCommand, CommandError
from tv.models import Card
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        Card.send_all()