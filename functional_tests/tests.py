from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_smoke(self):
        # Alice goes to main page and see
        self.browser.get(self.live_server_url)
        # in header: Betleague
        self.assertEqual(self.browser.title, 'Betleague')
        # and table in body:
        table = self.browser.find_element_by_id('results_table')
        table_header = table.find_element_by_tag_name('th')
        # with header: League table
        self.assertEqual('League table', table_header.text)