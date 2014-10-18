from django.contrib import admin
from .models import Artist, Album, Vote

@admin.register(Artist, Album, Vote)
class ModelAdmin(admin.ModelAdmin):
    pass
