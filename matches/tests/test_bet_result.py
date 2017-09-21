from unittest import TestCase

from matches.bet_result import calc_bet_result


class BetResultTest(TestCase):
    def test_any_wrong_bet(self):
        result = calc_bet_result(home_bet=0, away_bet=0, home_score=4, away_score=3)
        self.assertEqual(result, 1)

    def test_one_team_goals_guessed_bet(self):
        result = calc_bet_result(home_bet=0, away_bet=3, home_score=4, away_score=3)
        self.assertEqual(result, 2)

    def test_total_goals_guessed_not_less_4_bet(self):
        result = calc_bet_result(home_bet=2, away_bet=2, home_score=4, away_score=0)
        self.assertEqual(result, 2)

    def test_total_goals_guessed_less_4_bet(self):
        result = calc_bet_result(home_bet=1, away_bet=2, home_score=2, away_score=1)
        self.assertEqual(result, 1)

    def test_result_guessed_win_bet(self):
        result = calc_bet_result(home_bet=2, away_bet=0, home_score=4, away_score=3)
        self.assertEqual(result, 3)

    def test_result_and_total_goals_guessed_bet(self):
        result = calc_bet_result(home_bet=5, away_bet=2, home_score=4, away_score=3)
        self.assertEqual(result, 5)

    def test_result_and_one_team_goals_guessed_bet(self):
        result = calc_bet_result(home_bet=5, away_bet=3, home_score=4, away_score=3)
        self.assertEqual(result, 5)

    def test_goal_difference_guessed_bet(self):
        result = calc_bet_result(home_bet=1, away_bet=0, home_score=4, away_score=3)
        self.assertEqual(result, 6)

    def test_score_guessed_bet(self):
        result = calc_bet_result(home_bet=4, away_bet=3, home_score=4, away_score=3)
        self.assertEqual(result, 12)
