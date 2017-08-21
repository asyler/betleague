from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from accounts.factories import UserFactory
from competitions.views import league
from matches.factories import MatchFactory, BetFactory, FutureMatchFactory
from matches.models import Match


class LeaguePageTest(TestCase):
    def test_is_home_page(self):
        view = resolve('/')
        self.assertEqual(view.func, league)

    def test_uses_league_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'league.html')

    def test_passes_matches_to_template(self):
        matches = Match.objects.all()
        response = self.client.get('/')
        self.assertIn('matches', response.context)

    def test_passes_users_to_template(self):
        users = User.objects.all()
        response = self.client.get('/')
        self.assertIn('users', response.context)