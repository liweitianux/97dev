# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import logout, views as auth_views
from django.shortcuts import redirect, render_to_response


admin.autodiscover()
urlpatterns = patterns("",
	url(r"^admin/", include(admin.site.urls)),
	(r"^site_media/(?P<path>.*)$", "django.views.static.serve", {"document_root": "./media/"}),
)

def _logout(request, **kwargs):
    logout(request)
    return redirect('/')

urlpatterns += patterns("",
	url(r"^$", direct_to_template, {"template": "index.html"}, name="index"),
)

urlpatterns += patterns("info.views",
    url(r"^query\/?$", "query"),)

urlpatterns += patterns("",
    url(r"^blog/", include('sciblog.urls')),
    url(r"^accounts/", include('profile.urls')),
                       )
def page_not_found(request):
    return render_to_response('./templates/404.html')


## apps/indicator
urlpatterns += patterns('',
    url(r'^indicator/', include('indicator.urls')),
)


## search (haystack)
urlpatterns += patterns('',
    url(r'^search/', include('haystack.urls')),
)


