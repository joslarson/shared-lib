from django.contrib import admin
from .models import Artist, Album, Vote, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)


@admin.register(Artist, Vote)
class ModelAdmin(admin.ModelAdmin):
    pass


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
