from django.urls import reverse
from selenium.common.exceptions import NoSuchElementException

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTest
from functional_tests.pages.matches import MatchesPage
from functional_tests.pages.nav import NavPage
from matches.factories import FutureMatchFactory, PastMatchFactory, BetFactory


class SmokeTest(FunctionalTest):
    def test_home_page_smoke(self):
        # Ugo goes to main page and see
        self.browser.get(self.live_server_url+reverse('matches'))
        # in header: Betleague
        self.assertEqual(self.browser.title, 'Betleague')
        # and table in body:

        MatchesPage(self).get_table()  # should not raise


class MatchesTableTest(FunctionalTest):
    def setUp(self):
        self.url = self.live_server_url+reverse('matches')

        super().setUp(set_up_data = True)

    def test_page_shows_matches(self):
        # Ugo goes to main page and see
        self.browser.get(self.url)
        # column with mathces
        Page = MatchesPage(self)
        matches = Page.get_matches()
        self.assertEqual(len(matches), 4)
        # with match date, time, away and home teams
        self.assertEqual(Page.get_match_info(matches[0], 'home_team'), 'Bordo')
        self.assertEqual(Page.get_match_info(matches[1], 'away_team'), 'Ajax')
        self.assertEqual(Page.get_match_info(matches[3], 'date'), '09.01.2047')
        self.assertEqual(Page.get_match_info(matches[3], 'time'), '07:04')  # using timezone

    def test_page_shows_users(self):
        # Ugo goes to main page and see
        self.browser.get(self.url)
        # row with users
        Page = MatchesPage(self)
        users = Page.get_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(Page.get_user_username(users[0]), 'ugo')
        self.assertEqual(Page.get_user_username(users[1]), 'ada')

    def test_page_shows_users_bets_for_future_matches(self):
        # Ugo goes to main page and see
        self.browser.get(self.url)
        # his bet he placed before on match Ajax-Barcelona.
        Page = MatchesPage(self)
        bet = Page.find_bet('Ajax', 'Barcelona', 'ugo')
        self.assertEqual(bet.text, '2 - 1')
        # Also he notices bet from ada on Bordo-Chelsea
        bet = Page.find_bet('Ajax', 'Barcelona', 'ada')
        self.assertEqual(bet.text, '4 - 0')

    def test_page_shows_points_for_past_matches_with_results(self):
        # Ugo goes to main page and see
        self.browser.get(self.url)
        # an empty cell for Bordo-Chelsea, because he didn't bet that match
        Page = MatchesPage(self)
        bet_result = Page.find_bet_result('Bordo', 'Chelsea', 'ugo')
        self.assertEqual(bet_result.text, '')
        # and points for same match from ada.
        bet_result = Page.find_bet_result('Bordo', 'Chelsea', 'ada')
        self.assertEqual(bet_result.text, '12')

    def test_page_shows_bet_for_past_matches_without_results(self):
        # Ugo goes to main page and see
        self.browser.get(self.url)
        # an empty cell for Chelsea-Ajax, because he didn't bet that match
        Page = MatchesPage(self)
        bet_result = Page.find_bet('Chelsea', 'Ajax', 'ugo')
        self.assertEqual(bet_result.text, '')
        # and bet for same match from ada.
        bet_result = Page.find_bet('Chelsea', 'Ajax', 'ada')
        self.assertEqual(bet_result.text, '0 - 0')

    def test_page_shows_total_row(self):
        # Ugo goes to main page
        self.browser.get(self.url)
        Page = MatchesPage(self)
        # and see total points for all users
        self.assertEqual(Page.get_total('ugo'), '1')
        self.assertEqual(Page.get_total('ada'), '24')

    def test_cant_be_navigated_to_user_bets_if_not_authenticated(self):
        # Ugo goes to main page
        self.browser.get(self.url)
        # And he does not see button 'My bets'
        Page = NavPage(self)
        with self.assertRaises(NoSuchElementException):
            Page.get_user_bets_link().click()

    def test_12_points_are_highlighted(self):
        # Ugo goes to main page
        self.browser.get(self.url)
        Page = MatchesPage(self)
        # and see that 12 points cell is highlighted
        bet_result = Page.find_bet_result('Bordo', 'Chelsea', 'ada')
        self.assertEqual(bet_result.text, '12')
        self.assertIn('highlighted',bet_result.get_attribute('class'))
        # and not 12 - not highlighted
        bet_result = Page.find_bet_result('Bordo', 'Ajax', 'ugo')
        self.assertNotEqual(bet_result.text, '12')
        self.assertNotIn('highlighted', bet_result.get_attribute('class'))

    def test_switching_between_bets_and_points(self):
        # Ugo goes to main page
        self.browser.get(self.url)
        Page = MatchesPage(self)
        # and see switcher in position for showing points
        self.wait_for(lambda : self.assertTrue(Page.switcher_is_on()))
        # and points for past matches are shown
        bet_result = Page.find_bet_result('Bordo', 'Chelsea', 'ada')
        self.assertEqual(bet_result.text, '12')
        # He switches it to bets position
        Page.switcher_click()
        # and now sees bets for past matches
        self.assertFalse(Page.switcher_is_on())
        bet = Page.find_bet('Bordo', 'Chelsea', 'ada')
        self.assertEqual(bet.text, '2 - 0')

    def test_page_shows_results_col(self):
        # Ugo goes to main page
        self.browser.get(self.url)
        Page = MatchesPage(self)
        # and see results for past_matches
        self.assertEqual(Page.get_result('Bordo','Chelsea'), '2 - 0')

    def test_past_matches_with_results_are_highlighted(self):
        # Ugo goes to main page
        self.browser.get(self.url)
        Page = MatchesPage(self)
        # and see results for past_matches
        self.assertIn('past', Page.get_matches()[0].get_attribute('class'))
        self.assertIn('past', Page.get_matches()[1].get_attribute('class'))
        self.assertNotIn('past', Page.get_matches()[2].get_attribute('class'))
        self.assertNotIn('past', Page.get_matches()[3].get_attribute('class'))