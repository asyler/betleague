from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from matches.factories import PastMatchFactory, BetFactory, FutureMatchFactory
from matches.models import Match, Bet


class UserBetsPageTest(TestCase):
    def setUp(self):
        self.url = reverse('user_bets')
        self.future_match1 = FutureMatchFactory.create()
        self.user = UserFactory.create()
        BetFactory.create(match=self.future_match1, user=self.user, home_score=2, away_score=1)
        self.client.login(username=self.user.username, password=self.user.raw_password)

    def test_uses_league_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user_bets.html')

    def test_passes_matches_to_template(self):
        matches = Match.objects.all()
        response = self.client.get(self.url)
        self.assertIn('matches', response.context)

    def test_matches_contain_bets(self):
        response = self.client.get(self.url)
        self.assertEqual('2 - 1', str(response.context['matches'][0].bet))

    def test_POST_redirects_to_same_page(self):
        response = self.client.post(self.url)
        self.assertRedirects(response,self.url)

    def test_POST_saves_bets(self):
        self.client.post(self.url, data={
            'match_1': '2 - 0'
        })
        bet = Bet.objects.filter(user=self.user, match=self.future_match1).first()
        self.assertEqual(str(bet),'2 - 0')

    def test_for_invalid_input_invalid_input_not_saves(self):
        self.client.post(self.url, data={
            'match_1': '2 0'
        })

    def test_for_invalid_input_other_input_saves(self):
        self.fail()

    def test_for_invalid_input_show_erorrs(self):
        self.fail()

    def test_for_future_mathces_is_not_valid(self):
        self.fail()

class UserBetsPageUnathorized(TestCase):
    def test_page_view_redirects_unathorized_user(self):
        url = reverse('user_bets')
        response = self.client.get(url)
        self.assertIn('/accounts/login', response.url)