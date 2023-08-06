"""
Test custom Django managment commands.
"""
# mock database behavior to simulate it
from unittest.mock import patch
# possible errors when trying to connect to a database when it isn't ready
from psycopg2 import OperationalError as Psycopg2Error
# Allow to call a command to test
from django.core.management import call_command
# Excpection might happen
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# Mock the behavior of the database using check method
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self,patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value= True

        # check if the command is revokable and the result
        call_command('wait_for_db')

        # check if check method is called
        patched_check.assert_called_once_with(database=['default'])

    def wait_for_db_delay(self, patched_check):
        """Test waiting for databases when getting OperationalError and try again"""
        # first two times mocked method raise a Psycopg2Error
        # first two times raise Psycopg2Error and the next three times raise OperationalError
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        