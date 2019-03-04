from unittest.mock import patch, call

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from accounts.factories import UserFactory
from matches.factories import PastMatchFactory, FutureMatchFactory, BetFactory
from matches.models import Match, Bet


class MatchModelTest(TestCase):
    def test_cant_be_without_fields(self):
        match = Match()
        with self.assertRaises(ValidationError):
            match.full_clean()

    def test_has_is_in_future_attr(self):
        past_match = PastMatchFactory.create()
        future_match = FutureMatchFactory.create()

        self.assertTrue(future_match.in_future)
        self.assertFalse(past_match.in_future)

    def test_can_be_without_scores(self):
        match = FutureMatchFactory.create()
        match.full_clean()  # should not raise

    def test_default_score_values(self):
        match = Match()
        self.assertEqual(match.home_score, None)
        self.assertEqual(match.away_score, None)

    @patch('matches.models.Match.save')
    def test_set_score_calls_save_model_for_past_match(self, mock_save):
        match = PastMatchFactory.create()
        mock_save.reset_mock()

        match.set_score(home_score=1, away_score=2)

        self.assertTrue(mock_save.called)

    @patch('matches.models.Match.save')
    def test_set_score_doesnt_call_save_model_for_future_match(self, mock_save):
        match = FutureMatchFactory.create()
        mock_save.reset_mock()

        match.set_score(home_score=1, away_score=2)

        self.assertFalse(mock_save.called)

    def test_has_result_true_for_past_match_with_result(self):
        match = PastMatchFactory.create()
        self.assertTrue(match.has_result)

    def test_has_result_false_for_past_match_without_result(self):
        match = PastMatchFactory.create(home_score=None, away_score=None)
        self.assertFalse(match.has_result)

    def test_has_result_false_for_future_match(self):
        match = FutureMatchFactory.create()
        self.assertFalse(match.has_result)

    def test_has_string_representation(self):
        match = PastMatchFactory(
            home_team='A', away_team='B',
            home_score=0, away_score=1
        )
        self.assertEqual(str(match), 'A 0 - 1 B')

    def test_match_without_result_has_empty_string_representation(self):
        match = PastMatchFactory(
            home_team='A', away_team='B',
            home_score=None, away_score=None
        )
        self.assertEqual(str(match), 'A - B')

    def test_match_has_result_property(self):
        match = PastMatchFactory(home_score=0, away_score=1)
        self.assertEqual(match.result, '0 - 1')

    def test_match_has_result_property_for_no_result(self):
        match = PastMatchFactory(home_score=None, away_score=None)
        self.assertEqual(match.result, '')

    @patch('matches.models.Bet.set_result')
    def test_match_update_bets_calls_set_result_for_every_bet(self, mock_set_result):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        match = PastMatchFactory(home_score=1, away_score=2)
        bet1 = BetFactory(match=match, user=user1)
        BetFactory(match=match, user=user2)
        match.update_bets()
        self.assertEqual(mock_set_result.call_count,2)

    @patch('matches.models.Match.update_bets')
    def test_match_saves_with_scores_calls_update_bets(self, mock_update_bets):
        match = PastMatchFactory(home_score=None, away_score=None)
        match.home_score = 1
        match.home_score = 1
        match.save()
        self.assertTrue(mock_update_bets.called)

class BetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.past_match = PastMatchFactory.create()
        cls.future_match = FutureMatchFactory.create()
        cls.user = UserFactory.create()

    def test_should_contain_match(self):
        with self.assertRaises(IntegrityError):
            BetFactory(user=self.user)

    def test_should_contain_user(self):
        with self.assertRaises(IntegrityError):
            BetFactory(match=self.past_match)

    def test_invalid_incorrect_score(self):
        bet = Bet(home_score='two', away_score=1, match=self.future_match, user=self.user)
        with self.assertRaises(ValidationError):
            bet.full_clean()

    def test_valid_correct_score(self):
        bet = Bet(home_score=2, away_score=1, match=self.future_match, user=self.user)
        bet.full_clean()
        # should not raise

    def test_valid_for_future_matches(self):
        bet = BetFactory.create(match=self.future_match, user=self.user)
        bet.full_clean()
        # should not raise

    def test_invalid_for_past_matches(self):
        bet = BetFactory.create(match=self.past_match, user=self.user)
        with self.assertRaises(ValidationError):
            bet.full_clean()

    def test_has_string_representation(self):
        bet = BetFactory(home_score=0, away_score=1, match=self.past_match, user=self.user)
        self.assertEqual(str(bet), '0 - 1')

    def test_empty_bet_has_string_representation(self):
        bet = Bet(match=self.past_match, user=self.user)
        self.assertEqual(str(bet), '')

    def test_result_field_can_be_black(self):
        bet = BetFactory.create(home_score=2, away_score=1, match=self.past_match, user=self.user)
        self.assertEqual(bet.result, None)

    @patch('matches.bet_result.calc_bet_result')
    def test_bet_save_doesnt_calls_calc_result_func(self, mock_calc_bet_result):
        match = FutureMatchFactory.create()
        BetFactory.build(home_score=2, away_score=1, match=match, user=self.user)

        self.assertFalse(mock_calc_bet_result.called, False)

    @patch('matches.bet_result.calc_bet_result')
    def test_past_match_set_score_calls_calc_result_func_for_all_match_bets(self, mock_calc_bet_result):
        match = PastMatchFactory.create(home_score=None, away_score=None)
        user2 = UserFactory.create()
        BetFactory.create(home_score=4, away_score=3, match=match, user=self.user)
        BetFactory.create(home_score=2, away_score=1, match=match, user=user2)
        mock_calc_bet_result.return_value = 12
        self.assertFalse(mock_calc_bet_result.called)

        match.set_score(home_score=2, away_score=1)

        self.assertEqual(mock_calc_bet_result.call_count, 2)
        mock_calc_bet_result.assert_has_calls([
            call(
                home_bet=4, away_bet=3, home_score=2, away_score=1,
                shootout_winner=None, shootout_bet=None,
            ),
            call(
                home_bet=2, away_bet=1, home_score=2, away_score=1,
                shootout_winner=None, shootout_bet=None,
            )
        ])

    def test_past_match_set_score_set_all_match_bets_results(self):
        match = PastMatchFactory.create(home_score=None, away_score=None)
        user2 = UserFactory.create()
        BetFactory.create(home_score=4, away_score=3, match=match, user=self.user)
        BetFactory.create(home_score=2, away_score=1, match=match, user=user2)

        match.set_score(home_score=2, away_score=1)

        self.assertEqual(Bet.objects.all()[0].result, 6)
        self.assertEqual(Bet.objects.all()[1].result, 12)

    def check_format(self, result):
        # pass match with 5-4
        bet = Bet(match=self.future_match)
        bet.set_bet(result)

        self.assertEqual(bet.home_score, 5)
        self.assertEqual(bet.away_score, 4)

    def test_check_formats(self):
        self.check_format('5-4')
        self.check_format('5 - 4')
        self.check_format('5 -4')
        self.check_format('  5-4 ')
        self.check_format('5:  4 ')

    def test_check_format_fail(self):
        with self.assertRaises(ValidationError):
            self.check_format('5=4')
