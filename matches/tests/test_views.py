from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.factories import UserFactory
from matches.factories import PastMatchFactory, BetFactory, FutureMatchFactory
from matches.models import Match, Bet, WRONG_BET_FORMAT_ERROR


class UserBetsPageTest(TestCase):
    url = reverse('user_bets')
    # fixtures = ['accounts/fixtures/users.json', 'matches/fixtures/data.json']

    @classmethod
    def setUpTestData(cls):
        cls.future_match1 = FutureMatchFactory.create(datetime = timezone.now() + timezone.timedelta(days=2))
        cls.future_match2 = FutureMatchFactory.create(datetime = timezone.now() + timezone.timedelta(days=1))
        cls.future_match3 = FutureMatchFactory.create(datetime = timezone.now() + timezone.timedelta(days=3))
        cls.user = UserFactory.create()


    def setUp(self):
        self.client.login(username=self.user.username, password=self.user.raw_password)

    def test_uses_league_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user_bets.html')

    def test_passes_matches_to_template(self):
        response = self.client.get(self.url)
        self.assertIn('matches', response.context)

    def test_matches_contain_bets(self):
        BetFactory.create(match=self.future_match1, user=self.user, home_score=2, away_score=1)
        response = self.client.get(self.url)
        self.assertEqual('2 - 1', str(response.context['matches'][1].bet))

    def test_POST_redirects_to_same_page(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, self.url)

    def test_POST_saves_bets(self):
        self.client.post(self.url, data={
            'match_1': '2 - 0'
        })
        bet = Bet.objects.filter(user=self.user, match=self.future_match1).first()
        self.assertEqual(str(bet), '2 - 0')

    def test_POST_edit_bets(self):
        self.client.post(self.url, data={
            'match_1': '2 - 0'
        })
        self.client.post(self.url, data={
            'match_1': '3 - 0'
        })
        bet = Bet.objects.filter(user=self.user, match=self.future_match1).first()
        self.assertEqual(str(bet), '3 - 0')

    def test_for_invalid_input_invalid_input_not_saves(self):
        self.client.post(self.url, data={
            'match_1': '2 0'
        })
        bet = Bet.objects.filter(user=self.user, match=self.future_match1).first()
        self.assertEqual(bet, None)

    def test_many_inputs_saves(self):
        self.client.post(self.url, data={
            'match_1': '2 - 0',
            'match_2': '3 - 0',
        })
        bet1 = Bet.objects.filter(user=self.user, match=self.future_match1).first()
        bet2 = Bet.objects.filter(user=self.user, match=self.future_match2).first()
        self.assertEqual(str(bet1), '2 - 0')
        self.assertEqual(str(bet2), '3 - 0')

    def test_for_invalid_input_other_input_saves(self):
        self.client.post(self.url, data={
            'match_1': '2 0',
            'match_2': '3 - 0',
        })
        bet1 = Bet.objects.filter(user=self.user, match=self.future_match1).first()
        bet2 = Bet.objects.filter(user=self.user, match=self.future_match2).first()
        self.assertEqual(bet1, None)
        self.assertEqual(str(bet2), '3 - 0')

    def test_for_invalid_input_show_errors(self):
        response = self.client.post(self.url, data={
            'match_1': '2 0'
        }, follow=True)
        self.assertIn(WRONG_BET_FORMAT_ERROR, list(response.context.get('messages'))[0].message)

    def test_for_past_matches_is_not_valid(self):
        past_match = PastMatchFactory.create()
        self.client.post(self.url, data={
            f'match_{past_match.id}': '2 - 0'
        })
        bet = Bet.objects.filter(user=self.user, match=past_match).first()
        self.assertEqual(bet, None)

    def test_for_empty_input_nor_saving_nor_raising_error(self):
        response = self.client.post(self.url, data={
            'match_1': ''
        }, follow=True)
        bet = Bet.objects.filter(user=self.user, match=self.future_match1).first()
        self.assertEqual(bet, None)
        self.assertEqual(1, len(response.context.get('messages'))) # one for saved successful

    def test_matches_are_sorted_by_datetime(self):
        response = self.client.get(self.url)
        response_matches = response.context['matches']
        self.assertEqual(response_matches[0],self.future_match2)
        self.assertEqual(response_matches[1],self.future_match1)
        self.assertEqual(response_matches[2],self.future_match3)

class UserBetsPageUnauthorized(TestCase):
    def test_page_view_redirects_unauthorized_user(self):
        url = reverse('user_bets')
        response = self.client.get(url)
        self.assertIn('/accounts/login', response.url)
