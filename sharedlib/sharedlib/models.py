from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    score = models.IntegerField(default=0)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    suggester = models.ForeignKey(User, related_name='suggested_albums')
    artist = models.ForeignKey(Artist, related_name='albums')
    title = models.CharField(max_length=255)
    year = models.IntegerField(max_length=4)
    is_explicit = models.BooleanField(default=False)
    external_link = models.TextField()
    image_url = models.TextField()
    vote_count = models.IntegerField(default=0)

    cost = models.IntegerField(null=True, blank=True)
    file_url = models.TextField(null=True, blank=True)
    purchaser = models.ForeignKey(User, related_name='purchased_albums',
                                  null=True, blank=True)

    def __unicode__(self):
        return "{0.title} by {0.artist.name} ({0.year})".format(self)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Album.objects.get(pk=self.pk)
            if orig.purchaser != self.purchaser:
                score = 0
                for album in self.purchaser.purchased_albums.all():
                    score += album.cost
                self.purchaser.profile.score = score
                self.purchaser.profile.save()
        super(Album, self).save(*args, **kwargs)


class Vote(models.Model):
    user = models.ForeignKey(User, related_name='votes')
    album = models.ForeignKey(Album, related_name='votes')

    def __unicode__(self):
        return '{user} -> {album}'.format(user=unicode(self.user),
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
