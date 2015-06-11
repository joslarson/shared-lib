from django.contrib import admin

from .models import Artist, Album, OwnedAlbum, Vote


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)


@admin.register(OwnedAlbum, Artist, Vote)
class ModelAdmin(admin.ModelAdmin):
    pass
