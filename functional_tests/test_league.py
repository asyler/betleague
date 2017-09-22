from django.urls import reverse
from selenium.common.exceptions import NoSuchElementException

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTest
from functional_tests.pages.league import LeaguePage
from functional_tests.pages.matches import MatchesPage
from functional_tests.pages.nav import NavPage
from matches.factories import FutureMatchFactory, PastMatchFactory, BetFactory


class LeagueTableTest(FunctionalTest):
    def setUp(self):
        self.page = LeaguePage(self)

        super().setUp(set_up_data=True)

        self.page.go()

    def test_league_table_shows_users(self):
        # Ugo goes to league page
        # and see every user
        self.page.find_user('ugo')
        self.page.find_user('ada')
        # should find and not raise

    def test_league_table_shows_users_matches_count(self):
        # Ugo goes to league page
        # and see matches user bet for every user
        self.assertEqual(self.page.find_user_matches_bet('ugo'), '2')
        self.assertEqual(self.page.find_user_matches_bet('ada'), '4')

    def test_league_table_shows_users_points(self):
        # Ugo goes to league page
        # and see user points for every user
        self.assertEqual(self.page.find_user_points('ugo'), '1')
        self.assertEqual(self.page.find_user_points('ada'), '24')

    def test_league_table_shows_users_12s(self):
        # Ugo goes to league page
        # and see count of 12 for every user
        self.assertEqual(self.page.find_user_12s('ugo'), '0')
        self.assertEqual(self.page.find_user_12s('ada'), '2')