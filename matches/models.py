from django.db import models

# Create your models here.
class Match(models.Model):
    home_team = models.TextField()
    away_team = models.TextField()
    datetime = models.DateTimeField()