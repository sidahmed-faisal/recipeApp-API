"""
Django command to wait for the database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2Error
# Error django throws when database isn't ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for databases."""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write('Wating for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(database =['default'])
                db_up=True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database Availabel!'))