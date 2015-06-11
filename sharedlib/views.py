import json

from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login_required
from django.views.decorators.csrf import requires_csrf_token

from django.core import serializers

from sharedlib.serializers import UserSerializer
from sharedlib.models import Album, OwnedAlbum, Vote, Artist
import spotify

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@requires_csrf_token
@login_required
def inbox(request):
    ranked_users = User.objects.all().order_by('-score')
    user_votes = [vote.album.pk for vote in request.user.votes.all()]
    shared_albums = (Album.objects.filter(sharer__isnull=False)
                     .order_by('-share_date', '-pk'))
    context = {'user': request.user,
               'user_votes': user_votes,
               'page': 'inbox',
               'ranked_users': ranked_users,
               'shared_albums': shared_albums}
    return render(request, 'inbox.html', context)


@login_required
def album(request):
    if request.method == 'POST':
        album = Album()
        album.artist = Artist.objects.get_or_create(
            name=request.POST.get('artist'))[0]
        album.title = request.POST.get('title')
        album.year = request.POST.get('year')
        album.is_explicit = request.POST.get('is_explicit') == 'true'
        album.external_link = request.POST.get('external_link')
        album.image_url = request.POST.get('image_url')
        album.sharer = request.user
        exists = Album.objects.filter(artist=album.artist,
                                      title=album.title,
                                      year=album.year).exists()
        if not exists:
            album.save()
            return HttpResponse(
                serializers.serialize('json',
                                      Album.objects.filter(pk=album.pk)),
                content_type="application/json",
                status=200)
        else:
            return HttpResponse('{"message": "Duplicat album."}',
                                content_type="application/json",
                                status=409)


@login_required
def album_search(request):
    if request.method == 'GET':
        r = spotify.search_albums(
            request.GET.get('album'), request.GET.get('artist'))
        return HttpResponse(json.dumps(r['data']),
                            content_type="application/json",
                            status=r['status'])


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
