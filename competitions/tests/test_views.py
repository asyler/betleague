from django.test import TestCase
from django.urls import resolve

from competitions.views import league
from matches.models import Match


class LeaguePageTest(TestCase):
    def test_is_home_page(self):
        view = resolve('/')
        self.assertEqual(view.func, league)

    def test_uses_league_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'league.html')

    def test_passes_models_to_template(self):
        matches = Match.objects.all()
        response = self.client.get('/')
        self.assertQuerysetEqual(response.context['matches'], matches)