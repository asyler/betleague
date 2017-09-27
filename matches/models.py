import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from django.utils import timezone

from . import bet_result

PAST_MATCH_ERROR = 'Can\'t bet for past match'
WRONG_BET_FORMAT_ERROR = 'Wrong bet format'

class EmptyBet(Exception):
     pass

def parse_score(score):
    match = re.match(r'\s*(\d+)\s*[-:]\s*(\d+)\s*', score)
    if not match:
        return None

    home_score = int(match.group(1))
    away_score = int(match.group(2))
    return home_score, away_score


class Match(models.Model):
    home_team = models.TextField()
    away_team = models.TextField()
    datetime = models.DateTimeField()
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    @property
    def in_future(self):
        return self.datetime > timezone.now()

    @property
    def has_result(self):
        return self.home_score is not None

    @property
    def result(self):
        if not self.has_result:
            return ''
        return f'{self.home_score} - {self.away_score}'

    def update_bets(self):
        [b.set_result() for b in self.bet_set.all()]

    def set_score(self, home_score, away_score):
        if not self.in_future:
            self.home_score = home_score
            self.away_score = away_score
            self.save()

    def __str__(self):
        home_score = f' {self.home_score}' if self.has_result else ''
        away_score = f'{self.away_score} ' if self.has_result else ''
        return '{}{} - {}{}'.format(self.home_team, home_score, away_score, self.away_team)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.home_score is not None:
            self.update_bets()


def validate_match_datetime(value):
    match = Match.objects.get(pk=value)
    if not match.in_future:
        raise ValidationError('Match is in future')


class Bet(models.Model):
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    match = models.ForeignKey(Match, validators=[validate_match_datetime])
    user = models.ForeignKey(User)
    result = models.IntegerField(null=True, blank=True)

    def set_result(self):
        self.result = bet_result.calc_bet_result(
            home_bet=self.home_score,
            away_bet=self.away_score,
            home_score=self.match.home_score,
            away_score=self.match.away_score,
        )
        self.save()

    def __str__(self):
        if self.home_score is None:
            return ''
        return '{} - {}'.format(self.home_score, self.away_score)

    def set_bet(self, result):
        if not self.match.in_future:
            raise ValidationError(PAST_MATCH_ERROR)

        if result=='':
            raise EmptyBet

        bet = parse_score(result)
        if bet:
            self.home_score = bet[0]
            self.away_score = bet[1]
        else:
            raise ValidationError(WRONG_BET_FORMAT_ERROR)
