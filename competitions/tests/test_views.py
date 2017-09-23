from django.test import TestCase
from django.urls import resolve, reverse

from accounts.factories import UserFactory
from competitions.views import matches
from matches.factories import PastMatchFactory


class MatchesPageTest(TestCase):
    url = reverse('matches')
    fixtures = ['accounts/fixtures/users.json', 'matches/fixtures/data.json']

    def setUp(self):
        self.response = self.client.get(self.url)

    def get_user(self, username):
        return next(filter(lambda user: user.username == username, self.response.context['users']))

    def test_uses_matches_template(self):
        self.assertTemplateUsed(self.response, 'matches.html')

    def test_passes_matches_to_template(self):
        self.assertIn('matches', self.response.context)

    def test_passes_users_to_template(self):
        response = self.client.get(self.url)
        self.assertIn('users', self.response.context)

    def test_provide_user_points(self):
        user = self.get_user('vladomar')
        self.assertEqual(74, user.total_points)

    def test_provide_correct_user_points_if_0(self):
        user = self.get_user('rybalkadenis')
        self.assertEqual(0, user.total_points)


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
        self.assertEqual(74, user.points)

    def test_provide_correct_user_points_if_0(self):
        user = self.get_user('rybalkadenis')
        self.assertEqual(0, user.points)

    def test_provide_user_matches_bet(self):
        user = self.get_user('vladomar')
        self.assertEqual(16, user.matches_bet)

    def test_provide_user_12s(self):
        user = self.get_user('vladomar')
        self.assertEqual(3, user.guess_hits)

    def test_provide_sorted_users(self):
        users = self.response.context['users']
        self.assertEqual(users[0].username, 'Vova')
        self.assertEqual(users[1].username, 'vladomar')