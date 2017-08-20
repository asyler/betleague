from django.shortcuts import render

# Create your views here.
from matches.models import Match


def league(request):
    matches = Match.objects.all()
    return render(request, 'league.html', {
        'matches': matches
    })