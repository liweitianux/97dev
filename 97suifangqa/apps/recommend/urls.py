# -*- coding: utf-8 -*-

"""
URL configuration for apps/recommend
"""

from django.conf.urls.defaults import *

from recommend import models as rm


urlpatterns = patterns('recommend.views',
    # app index
    url(r'^$',
        'recommend_index',
        name='recommend_index'),
)

