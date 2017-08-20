from functional_tests.base import FunctionalTest
from functional_tests.pages.league import LeaguePage


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