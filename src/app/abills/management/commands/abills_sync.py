from django.core.management.base import BaseCommand, CommandError
from tv.models import CardService

class Command(BaseCommand):

    def handle(self, *args, **options):
        css = CardService.objects.filter(extra__isnull=False)
        for cs in css:
            for link in cs.abills_links.all():
                link.sync()