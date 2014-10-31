from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from sharedlib.models import Album, Vote, UserProfile
from django.contrib.auth.views import login_required


@login_required
def home(request):
    ranked_users = [profile.user for profile in UserProfile.objects.all().order_by('-score')]
    user_votes = [vote.album.pk for vote in request.user.votes.all()]
    suggested = (Album.objects.filter(purchaser=None)
                 .order_by('-vote_count', 'artist', '-year'))
    purchased = (Album.objects.filter(purchaser__isnull=False)
                 .order_by('artist', '-year'))
    context = {'user': request.user, 'user_votes': user_votes,
               'ranked_users': ranked_users,
               'suggested': suggested, 'purchased': purchased}
    return render(request, 'home.html', context)


@login_required
def vote(request, album_id):
    if request.method == 'POST':
        user = request.user
        album = Album.objects.get(pk=album_id)
        action = request.POST.get('action')
        exists = Vote.objects.filter(album=album, user=user).exists()
        if action == 'increment' and not exists:
            Vote(user=user, album=album).save()
            return HttpResponse('{"message": "Vote posted successfully."}',
                                content_type="application/json",
                                status=200)
        elif action == 'decrement' and exists:
            Vote.objects.get(album=album, user=user).delete()
            return HttpResponse('{"message": "Vote removed successfully."}',
                                content_type="application/json",
                                status=200)
        else:
            return HttpResponse('{"message": "Unable to modify vote."}',
                                content_type="application/json",
                                status=400)
