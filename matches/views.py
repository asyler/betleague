import re
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.shortcuts import render, redirect

# Create your views here.
from matches.models import Match, Bet, EmptyBet


@login_required
def user_bets(request):
    if request.method == 'POST':
        data = defaultdict(dict)
        for key, value in request.POST.items():
            _match = re.match(r'^match_(\d+)$', key)
            _match_shootout = re.match(r'^match_(\d+)_shootout_winner$', key)

            if _match:
                match_id = _match.group(1)
                data[match_id]['result'] = value

            if _match_shootout:
                match_id = _match_shootout.group(1)
                data[match_id]['shootout_winner'] = value

        for match_id, match_result in data.items():
            result = match_result['result']
            shootout_result = match_result.get('shootout_winner', None)
            try:
                bet = Bet.objects.get(user=request.user, match__id=match_id)
            except Bet.DoesNotExist:
                bet = Bet(user=request.user, match_id=match_id)
            try:
                bet.set_bet(result, shootout_result)
                bet.save()
            except ValidationError as e:
                messages.error(request, e.message, extra_tags=match_id)
            except EmptyBet:
                pass


        messages.success(request, 'Saved', extra_tags='saved')
        return redirect('user_bets')

    matches = Match.objects.order_by('datetime').all()
    for match in matches:
        try:
            match.bet = Bet.objects.get(match=match, user=request.user)
        except Bet.DoesNotExist:
            match.bet = Bet(user=request.user, match=match)
    return render(request, 'user_bets.html', {
        'matches': matches
    })
