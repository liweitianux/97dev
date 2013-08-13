from django.conf.urls import patterns, url

from .views import  *

urlpatterns = patterns('',
        url(r'^login/?$', login, name = "login"),
        url(r'^logout/?$', logout, name = "logout"),
        url(r'^signup/?$', signup, name = "signup"),
                      )
