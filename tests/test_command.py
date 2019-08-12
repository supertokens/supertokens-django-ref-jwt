from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class RemoveOldTokenTest(TestCase):
    def test_command(self):
        out = StringIO()
        call_command('remove_old_tokens', stdout=out)
        self.assertEqual('Successfully removed old refresh tokens\n', out.getvalue())