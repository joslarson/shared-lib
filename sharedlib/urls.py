from rest_framework import routers
from django.conf.urls import patterns, include, url
from django.contrib import admin

from sharedlib import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',
    url(r'^$', 'sharedlib.views.inbox', name='inbox'),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/album_search.json$', 'sharedlib.views.album_search', name='album_search'),
    url(r'^api/album.json$', 'sharedlib.views.album', name='album'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^album/([0-9]+)/vote/$', 'sharedlib.views.vote', name='vote'),
    url(r'^admin/', include(admin.site.urls)),
)
