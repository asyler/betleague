import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from django.utils import timezone

from . import bet_result

PAST_MATCH_ERROR = 'Can\'t bet for past match'
WRONG_BET_FORMAT_ERROR = 'Wrong bet format'


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

    def set_score(self, home_score, away_score):
        if not self.in_future:
            self.home_score = home_score
            self.away_score = away_score
            self.save()

            [b.set_result() for b in self.bet_set.all()]


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
        return '{} - {}'.format(self.home_score, self.away_score)

    def set_bet(self, result):
        match = re.match(r'\s*(\d+)\s*[-:]\s*(\d+)\s*', result)
        if not self.match.in_future:
            raise ValidationError(PAST_MATCH_ERROR)
        elif match:
            self.home_score = int(match.group(1))
            self.away_score = int(match.group(2))
        else:
            raise ValidationError(WRONG_BET_FORMAT_ERROR)
