from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.utils import timezone


class Match(models.Model):
    home_team = models.TextField()
    away_team = models.TextField()
    datetime = models.DateTimeField()

    @property
    def in_future(self):
        return self.datetime > timezone.now()


def validate_match_datetime(value):
    match = Match.objects.get(pk=value)
    if not match.in_future:
        raise ValidationError('Match is in future')

class Bet(models.Model):
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    match = models.ForeignKey(Match, validators=[validate_match_datetime])
    user = models.ForeignKey(User)

    def __str__(self):
        return '{} - {}'.format(self.home_score, self.away_score)