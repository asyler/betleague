class UserBetsPage(object):
    def __init__(self, test):
        self.test = test
        self.url = self.test.live_server_url+'/my_bets'

    def go(self):
        self.test.browser.get(self.url)

    def get_matches(self):
        return self.test.browser \
            .find_elements_by_css_selector('div.match')

    def get_match_body(self, match):
        return match.find_element_by_class_name('bet').text

    def get_match_input(self, match):
        return match.find_element_by_tag_name('input')

    def press_save_button(self):
        self.test.browser.find_element_by_id('save_bets').click()