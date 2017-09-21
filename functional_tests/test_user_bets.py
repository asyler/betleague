from unittest import skip

from functional_tests.base import FunctionalTest
from functional_tests.pages.league import LeaguePage
from functional_tests.pages.nav import NavPage
from functional_tests.pages.user_bets import UserBetsPage
from matches.factories import FutureMatchFactory, PastMatchFactory, BetFactory


class UserBetsTest(FunctionalTest):
    def setUp(self):
        super().setUp()

        self.future_match = FutureMatchFactory.create(home_team='Ajax', away_team='Barcelona')
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
        self.assertEqual(len(matches), 3)

    def test_past_matches_show_only_bets(self):
        Page = UserBetsPage(self)
        # Ugo goes to My bets page
        Page.go()
        # He sees 2 past matches for now
        matches = Page.get_matches()
        # For both of them he sees his bet
        self.assertEqual(Page.get_match_body(matches[2]), '2 - 1')
        # and no input
        self.assertNotIn('input', Page.get_match_body(matches[1]))

    def test_future_matches_can_be_bet(self):
        Page = UserBetsPage(self)
        # Ugo goes to My bets page
        Page.go()
        # He sees input field for future match
        matches = Page.get_matches()
        input = Page.get_match_input(matches[0])
        # He sees his current bet on it
        self.assertEqual(input.get_attribute('value'), '5 - 1')
        # He changes his bet
        input.clear()
        input.send_keys('3 - 1')
        # and presses Save button
        Page.press_save_button()
        # Page reloads and now he sees same field with his new bet
        self.wait_for(
            lambda: self.assertEqual(Page.get_match_input(Page.get_matches()[0]).get_attribute('value'), '3 - 1'))
        # Now he goes to main league page
        self.browser.get(self.live_server_url)
        # and see same bet from him on the same match
        league_page = LeaguePage(self)
        matches = league_page.get_matches()
        bet = league_page.find_bet('Ajax', 'Barcelona', 'ugo')
        self.assertEqual(bet.text, '3 - 1')

    @skip
    def test_invalid_bets_results_to_errors(self):
        self.fail()
