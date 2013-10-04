# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('profile.views',
    url(r'^(?P<username>[a-zA-Z_][a-zA-Z0-9_]*)/$',
        'profile_view', name='profile_home'),
)

