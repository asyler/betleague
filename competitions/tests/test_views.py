from django.test import TestCase
from django.urls import resolve, reverse

from accounts.factories import UserFactory
from competitions.views import matches
from matches.factories import PastMatchFactory
from matches.models import Match


class MatchesPageTest(TestCase):
    url = reverse('matches')
    fixtures = ['accounts/fixtures/users.json', 'matches/fixtures/data.json']

    def get_user(self, username):
        return next(filter(lambda user: user.username == username, self.response.context['users']))

    def test_uses_matches_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'matches.html')

    def test_passes_matches_to_template(self):
        response = self.client.get(self.url)
        self.assertIn('matches', response.context)

    def test_passes_users_to_template(self):
        response = self.client.get(self.url)
        self.assertIn('users', response.context)

    def test_provide_user_points(self):
        self.response = self.client.get(self.url)
        user = self.get_user('vladomar')
        self.assertEqual(114, user.total_points)

    def test_provide_correct_user_points_if_0(self):
        self.response = self.client.get(self.url)
        user = self.get_user('rybalkadenis')
        self.assertEqual(0, user.total_points)

    def test_matches_are_sorted_by_datetime_after_set_score(self):
        match = Match.objects.filter(home_team='Карабах', away_team='Рома').get()
        match.set_score(1,1)

        response = self.client.get(self.url)
        response_matches = response.context['matches']
        self.assertEqual(response_matches[25], match)


class LeaguePageTest(TestCase):
    url = reverse('league')
    fixtures = ['accounts/fixtures/users.json', 'matches/fixtures/data.json']

    def setUp(self):
        self.response = self.client.get(self.url)

    def test_uses_league_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'league.html')

    def get_user(self, username):
        return next(filter(lambda user: user.username == username, self.response.context['users']))

    def test_passes_users_to_template(self):
        self.assertIn('users', self.response.context)

    def test_provide_user_points(self):
        user = self.get_user('vladomar')
        self.assertEqual(114, user.points)

    def test_provide_correct_user_points_if_0(self):
        user = self.get_user('rybalkadenis')
        self.assertEqual(0, user.points)

    def test_provide_user_matches_bet(self):
        user = self.get_user('vladomar')
        self.assertEqual(24, user.matches_bet)

    def test_provide_user_12s(self):
        user = self.get_user('vladomar')
        self.assertEqual(5, user.guess_hits)

    def test_provide_sorted_users(self):
        users = self.response.context['users']
        self.assertEqual(users[0].username, 'Vova')
        self.assertEqual(users[1].username, 'vladomar')