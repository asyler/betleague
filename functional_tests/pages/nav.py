class NavPage(object):
    def __init__(self, test):
        self.test = test

    def get_user_bets_link(self):
        return self.test.browser.find_element_by_link_text('My bets')
