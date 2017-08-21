from unittest import skip

from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTest
from functional_tests.pages.league import LeaguePage
from matches.factories import FutureMatchFactory, PastMatchFactory, BetFactory
from matches.models import Match


class SmokeTest(FunctionalTest):
    def test_home_page_smoke(self):
        # Ugo goes to main page and see
        self.browser.get(self.live_server_url)
        # in header: Betleague
        self.assertEqual(self.browser.title, 'Betleague')
        # and table in body:

        table = LeaguePage(self).get_league_table()
        table_header = table.find_element_by_tag_name('th')
        # with header: League table
        self.assertEqual('League table', table_header.text)


class LeagueTableTest(FunctionalTest):
    def setUp(self):
        self.future_match = FutureMatchFactory.create(datetime="2017-01-09 05:04+00:00")
        self.past_match = PastMatchFactory.create()

        self.user1 = UserFactory.create()
        self.user2 = UserFactory.create()

        self.bets = [
            [
                BetFactory.create(match=self.future_match, user=self.user1),
                BetFactory.create(match=self.future_match, user=self.user2),
            ], # future match
            [

            ] # past match
        ]

        super().setUp()

    def test_page_show_matches(self):
        # Ugo goes to main page and see
        self.browser.get(self.live_server_url)
        # column with mathces
        Page = LeaguePage(self)
        matches = Page.get_matches()
        self.assertEqual(len(matches), 2)
        # with match date, time, away and home teams
        self.assertEqual(Page.get_match_info(matches[0],'home_team'), self.future_match.home_team)
        self.assertEqual(Page.get_match_info(matches[1],'away_team'), self.past_match.away_team)
        self.assertEqual(Page.get_match_info(matches[0],'date'), '09.01.2017')
        self.assertEqual(Page.get_match_info(matches[0],'time'), '07:04') # using timezone

    def test_page_show_users(self):
        # Ugo goes to main page and see
        self.browser.get(self.live_server_url)
        # row with users
        Page = LeaguePage(self)
        users = Page.get_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(Page.get_user_username(users[0]), self.user1.username)
        self.assertEqual(Page.get_user_username(users[1]), self.user2.username)

    def test_page_show_users_bets_for_future_matches(self):
        # Ugo goes to main page and see
        self.browser.get(self.live_server_url)
        # his bet he placed before on match Ajax-Barcelona
        Page = LeaguePage(self)
        bet = Page.find_bet(self.future_match.home_team,self.future_match.away_team,self.user1.username)
        self.assertEqual(bet.text, '{} - {}'.format(self.bets[0][0].home_score,self.bets[0][0].away_score))
        # and empty cell for Bordo-Chelsea, because he didn't bet that match.
        bet = Page.find_bet(self.past_match.home_team,self.past_match.away_team, self.user1.username)
        self.assertEqual(bet.text, '')
        # Also he notices bet from ada on Bordo-Chelsea
        bet = Page.find_bet(self.future_match.home_team,self.future_match.away_team, self.user2.username)
        self.assertEqual(bet.text, '{} - {}'.format(self.bets[0][1].home_score,self.bets[0][1].away_score))

        with open('data.json','w+') as f:
            call_command('dumpdata', stdout=f)

    @skip
    def test_page_show_points_for_past_matches(self):
        self.fail('todo')

