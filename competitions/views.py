from django.shortcuts import render

# Create your views here.
def league(request):
    return render(request, 'league.html')