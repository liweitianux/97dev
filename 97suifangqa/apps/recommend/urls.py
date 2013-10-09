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
    # add/edit blog info
    url(r'add_edit/blog/(?P<blog_id>[1-9][0-9]*)/$',
        'add_edit_blog_info',
        name='add_edit_blog_info'),
    ## ajax
    # add/edit configs
    url(r'ajax/add_edit_configs/',
        'ajax_add_edit_configs',
        name='ajax_add_edit_configs'),
)

