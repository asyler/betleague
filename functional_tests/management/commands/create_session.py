from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['username'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=username+'666')
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key, user
