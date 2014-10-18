from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=255, required=True)
    artist = models.ForeignKey(Artist, required=True, related_name='albums')
    vote_count = models.IntegerField(default=0)
    cost = models.IntegerField()
    external_link = models.TextField()
    file_url = models.TextField()
    image_url = models.TextField()
    suggester = models.ForeignKey(User, related_name='suggested_albums',
                                  required=True)
    purchaser = models.ForeignKey(User, related_name='purchased_albums')

    def __unicode__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(User, related_name='votes')
    album = models.ForeignKey(Album, related_name='votes')

    def __unicode__(self):
        return '<Vote {user}:{album}>'.format(user=unicode(self.user),
                                              album=unicode(self.album))
    # update chached vote_count of self.album
    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)
        self.album.vote_count += 1
        self.album.save()

    def delete(self, *args, **kwargs):
        self.album.vote_count -= 1
        self.album.save()
        super(Vote, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ("user", "album")
