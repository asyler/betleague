class LeaguePage(object):
    def __init__(self, test):
        self.test = test

    def get_league_table(self):
        return self.test.browser.find_element_by_id('results_table')

    def get_matches(self):
        return self.test.browser\
            .find_element_by_tag_name('tbody')\
            .find_elements_by_tag_name('tr')

    def get_match_info(self, match, field):
        return match.find_element_by_class_name(field).text