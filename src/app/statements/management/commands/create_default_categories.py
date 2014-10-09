# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from django.core.management.base import BaseCommand, CommandError
from statements.models import Category, TYPE_CATV
from tv.models import PaymentSource
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


class Command(BaseCommand):
    help = 'Create default categories for each payment source'

    def handle(self, *args, **options):
        for source in PaymentSource.objects.all():
            if source.statements_categories.all().count() < 1:
                Category.objects.create(source=source, name=source.name, svc_type=TYPE_CATV)