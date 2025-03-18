import glob
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

FIXTURE_DIR = os.path.join(settings.BASE_DIR, "fixtures")


class Command(BaseCommand):
    help = "Load fixture data from JSON files"

    def handle(self, *args, **options):
        fixture_pattern = os.path.join(FIXTURE_DIR, "**", "*.json")

        fixture_files = glob.glob(fixture_pattern, recursive=True)
        fixture_files.sort()

        for fixture_file in fixture_files:
            call_command("loaddata", fixture_file)
