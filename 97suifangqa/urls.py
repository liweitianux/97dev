# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import logout, views as auth_views
from django.shortcuts import redirect, render

from django.conf import settings

# staticfiles
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns("",
	url(r"^admin/", include(admin.site.urls)),
	(r"^site_media/(?P<path>.*)$", "django.views.static.serve", {"document_root": "./media/"}),
)

def _logout(request, **kwargs):
    logout(request)
    return redirect('/')

urlpatterns += patterns("",
    url(r"^$", direct_to_template,
        {"template": "index.html"}, name="index"),
)

urlpatterns += patterns("info.views",
    url(r"^query\/?$", "query"),
)

urlpatterns += patterns('',
    url(r'^blog/', include('sciblog.urls')),
    url(r'^accounts/', include('sfaccount.urls')),
    url(r'^profile/', include('profile.urls')),
    url(r'^indicator/', include('indicator.urls')),
    url(r'^recommend/', include('recommend.urls')),
)

def page_not_found(request):
    return render(request, './templates/404.html')


## search (haystack)
urlpatterns += patterns('',
    url(r'^search/', include('haystack.urls')),
)


## test 'media' settings
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        # media
        url(r'^media/(?P<path>.*)$',
            'serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

## staticfiles
urlpatterns += staticfiles_urlpatterns()

