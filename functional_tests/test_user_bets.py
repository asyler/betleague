from unittest import skip

from functional_tests.base import FunctionalTest
from functional_tests.pages.league import LeaguePage
from functional_tests.pages.nav import NavPage
from functional_tests.pages.user_bets import UserBetsPage
from matches.factories import FutureMatchFactory, PastMatchFactory, BetFactory
from matches.models import WRONG_BET_FORMAT_ERROR


class UserBetsTest(FunctionalTest):
    def setUp(self):
        super().setUp()

        self.future_match = FutureMatchFactory.create(home_team='Ajax', away_team='Barcelona')
        self.future_match2 = FutureMatchFactory.create(home_team='Barcelona', away_team='Ajax')
        self.past_match = PastMatchFactory.create()
        self.past_match2 = PastMatchFactory.create()

        # Ugo is a logged-in user
        user = self.create_pre_authenticated_session('ugo')

        self.bets = [
            BetFactory.create(match=self.future_match, user=user, home_score=5, away_score=1),
            BetFactory.create(match=self.past_match, user=user, home_score=1, away_score=1),
            BetFactory.create(match=self.past_match2, user=user, home_score=2, away_score=1),
        ]

    def test_can_be_navigated_from_home_page_if_authenticated(self):
        # Ugo goes to main page
        self.browser.get(self.live_server_url)
        # He sees button 'My bets'
        Page = NavPage(self)
        # He clicks it
        Page.get_user_bets_link().click()
        # and now he is on his bets page
        self.assertIn('/my_bets', self.browser.current_url)

    def test_page_show_matches(self):
        Page = UserBetsPage(self)
        # Ugo goes to My bets page
        Page.go()
        # He sees table all with mathces
        matches = Page.get_matches()
        self.assertEqual(len(matches), 4)

    def test_past_matches_show_only_bets(self):
        Page = UserBetsPage(self)
        # Ugo goes to My bets page
        Page.go()
        # He sees 2 past matches for now
        matches = Page.get_matches()
        # For both of them he sees his bet
        self.assertEqual(Page.get_match_body(matches[3]), '2 - 1')
        # and no input
        self.assertNotIn('input', Page.get_match_body(matches[2]))

    def test_future_matches_can_be_bet(self):
        Page = UserBetsPage(self)
        # Ugo goes to My bets page
        Page.go()
        # He sees input fields for two future matches
        matches = Page.get_matches()
        input1 = Page.get_match_input(matches[0])
        input2 = Page.get_match_input(matches[1])
        # He sees his current bet on first match it
        self.assertEqual(input1.get_attribute('value'), '5 - 1')
        # and no bet on another match
        self.assertEqual(input2.get_attribute('value'), '')
        # He changes his bet on first match
        input1.clear()
        input1.send_keys('3 - 1')
        # and places bet for second one
        input2.send_keys('1 - 1')
        # and presses Save button
        Page.press_save_button()
        # Page reloads and now he sees same fields with his new bets
        self.wait_for(
            lambda: self.assertEqual(Page.get_match_input(Page.get_matches()[0]).get_attribute('value'), '3 - 1'))
        # Now he goes to main league page
        self.browser.get(self.live_server_url)
        # and see same bets from him on the same matches
        league_page = LeaguePage(self)
        matches = league_page.get_matches()
        bet1 = league_page.find_bet('Ajax', 'Barcelona', 'ugo')
        bet2 = league_page.find_bet('Barcelona', 'Ajax', 'ugo')
        self.assertEqual(bet1.text, '3 - 1')
        self.assertEqual(bet2.text, '1 - 1')

    def test_invalid_bets_results_to_errors(self):
        Page = UserBetsPage(self)
        # Ugo goes to My bets page
        Page.go()
        # He sees input fields for two future matches
        matches = Page.get_matches()
        input1 = Page.get_match_input(matches[0])
        input2 = Page.get_match_input(matches[1])
        # He places correct bet on first match
        input1.clear()
        input1.send_keys('3 - 1')
        # He places incorrect bet on second match
        input2.send_keys('1 = 1')
        # and presses Save button
        Page.press_save_button()
        # Page reloads and now he sees first match with placed bet
        self.wait_for(
            lambda: self.assertEqual(Page.get_match_input(Page.get_matches()[0]).get_attribute('value'), '3 - 1'))
        # and second match with no bet as it was
        self.assertEqual(Page.get_match_input(Page.get_matches()[1]).get_attribute('value'), '')
        # and error near it
        self.assertEqual(Page.get_match_error(Page.get_matches()[1]), WRONG_BET_FORMAT_ERROR)
