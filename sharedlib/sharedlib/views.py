from django.shortcuts import render
from django.contrib.auth.models import User
from sharedlib.models import Artist, Album, Vote
import json

def index(request):
    suggested = Album.objects.filter(purchaser=None).order_by('-vote_count')
    purchased = Album.objects.filter(purchaser=None).order_by
    context = {'suggested': suggested, 'purchased': purchased }
    return render(request, 'comb/index.html', context)
