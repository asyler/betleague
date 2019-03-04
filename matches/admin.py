# Register your models here.
from django.contrib import admin

from matches.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'home_team', 'away_team', 'result')
    ordering = ('datetime',)
