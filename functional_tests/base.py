import os
import time
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from accounts.factories import UserFactory
from functional_tests.management.commands.create_session import create_pre_authenticated_session
from matches.factories import FutureMatchFactory, PastMatchFactory, BetFactory

MAX_WAIT = 10
SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self, set_up_data = False):
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(800, 600)

        if set_up_data:
            self.setUpData()

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()

    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    @wait
    def wait_to_be_logged_in(self):
        self.browser.find_element_by_link_text('Log out')

    @wait
    def wait_to_be_logged_out(self):
        self.browser.find_element_by_link_text('Login')

    @wait
    def wait_for(self, fn):
        return fn()

    def create_pre_authenticated_session(self, username):
        session_key, user = create_pre_authenticated_session(username)
        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")

        cookies = dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            secure=False,
            path='/',
            domain='localhost'
        )

        try:
            self.browser.add_cookie(cookies)
        except WebDriverException:
            # despite exception cookie finally is set up
            pass

        return user

    def setUpData(self):
        self.past_match = PastMatchFactory.create(home_team='Bordo', away_team='Chelsea')
        self.past_match2 = PastMatchFactory.create(home_team='Bordo', away_team='Ajax')
        self.past_match3 = PastMatchFactory.create(home_team='Chelsea', away_team='Ajax',
                                                   home_score=None, away_score=None)
        self.future_match = FutureMatchFactory.create(home_team='Ajax', away_team='Barcelona',
                                                      datetime="2047-01-09 05:04+00:00")

        self.user1 = UserFactory.create(username='ugo')
        self.user2 = UserFactory.create(username='ada')

        self.bets = [
            [
                BetFactory.create(match=self.future_match, user=self.user1, home_score=2, away_score=1),
                BetFactory.create(match=self.future_match, user=self.user2, home_score=4, away_score=0),
            ],  # future match
            [
                None,
                BetFactory.create(match=self.past_match, user=self.user2, home_score=2, away_score=0),
            ],  # past match
            [
                BetFactory.create(match=self.past_match2, user=self.user1, home_score=1, away_score=3),
                BetFactory.create(match=self.past_match2, user=self.user2, home_score=0, away_score=0),
            ],
            [
                None,
                BetFactory.create(match=self.past_match3, user=self.user2, home_score=0, away_score=0),
            ]
        ]

        self.past_match.set_score(home_score=2, away_score=0)
        self.past_match2.set_score(home_score=0, away_score=0)

