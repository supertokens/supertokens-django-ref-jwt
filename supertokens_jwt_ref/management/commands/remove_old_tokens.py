from django.core.management.base import BaseCommand, CommandError
from supertokens_jwt_ref.session_helper import remove_expired_tokens


class Command(BaseCommand):

    help = 'remove old expired tokens from refresh token table'

    def handle(self, *args, **kwargs):
        try:
            remove_expired_tokens()
        except Exception as e:
            raise CommandError(e) from e

        self.stdout.write('Successfully removed old refresh tokens')
