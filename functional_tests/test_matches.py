from django.utils import timezone

from functional_tests.base import FunctionalTest
from functional_tests.pages.league import LeaguePage
from matches.models import Match


class MatchesTest(FunctionalTest):
    def setUp(self):
        self.db = []
        self.db.append(Match.objects.create(home_team='Ajax',away_team='Barcelona', datetime="2017-01-09 05:04+00:00"))
        self.db.append(Match.objects.create(home_team='Bordo',away_team='Chelsea', datetime=timezone.now()))
        super().setUp()

    def test_home_page_show_matches(self):
        # Ugo goes to main page and see
        self.browser.get(self.live_server_url)
        # column with mathces
        Page = LeaguePage(self)
        matches = Page.get_matches()
        self.assertEqual(len(matches), 2)
        # with match date, time, away and home teams
        self.assertEqual(Page.get_match_info(matches[0],'home_team'), self.db[0].home_team)
        self.assertEqual(Page.get_match_info(matches[1],'away_team'), self.db[1].away_team)
        self.assertEqual(Page.get_match_info(matches[0],'date'), '09.01.2017')
        self.assertEqual(Page.get_match_info(matches[0],'time'), '07:04') # using timezone