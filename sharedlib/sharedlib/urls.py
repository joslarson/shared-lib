from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sharedlib.views.home', name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^album/([0-9]+)/vote/$', 'sharedlib.views.vote', name='vote'),
    url(r'^admin/', include(admin.site.urls)),
)
