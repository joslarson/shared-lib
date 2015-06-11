from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    sharer = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='shared_albums')
    share_date = models.DateTimeField(auto_now_add=True)

    artist = models.ForeignKey(Artist, related_name='albums')
    title = models.CharField(max_length=255)
    year = models.IntegerField(max_length=4)
    is_explicit = models.BooleanField(default=False)
    external_link = models.TextField()
    image_url = models.TextField()
    vote_count = models.IntegerField(default=0)

    def __unicode__(self):
        return "{0.title} by {0.artist.name} ({0.year})".format(self)

    def save(self, *args, **kwargs):
        affected_users = []
        if self.pk is not None:
            orig = Album.objects.get(pk=self.pk)
            if orig.sharer is not None:
                affected_users.append(orig.sharer)
        if self.sharer is not None:
            affected_users.append(self.sharer)

        super(Album, self).save(*args, **kwargs)
        if self.sharer is not None:
            Vote.objects.get_or_create(user=self.sharer, album=self)[0].save()

        for user in affected_users:
            user.refresh_score()


class OwnedAlbum(Album):
    purchaser = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='purchased_albums',
                                  null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    file_url = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        affected_users = []
        if self.pk is not None:
            orig = Album.objects.get(pk=self.pk)
            if orig.purchaser is not None:
                affected_users.append(orig.purchaser)
        if self.purchaser is not None:
            affected_users.append(self.purchaser)
        super(Album, self).save(*args, **kwargs)
        for user in affected_users:
            user.refresh_score()


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes')
    album = models.ForeignKey(Album, related_name='votes')

    def __unicode__(self):
        return '{user} -> {album}'.format(user=unicode(self.user),
                                          album=unicode(self.album))

    # update chached vote_count of self.album
    def save(self, *args, **kwargs):
        is_create = not self.pk
        super(Vote, self).save(*args, **kwargs)
        if is_create:
            self.album.vote_count += 1
            self.album.save()

    def delete(self, *args, **kwargs):
        super(Vote, self).delete(*args, **kwargs)
        self.album.vote_count -= 1
        self.album.save()

    class Meta:
        unique_together = ("user", "album")
