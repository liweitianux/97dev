# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from sciblog.models import SciBlog, BlogAnnotation
from sciblog.views import  *


blog_blocks = '|'.join(['source','abstract', 'knowledge','follow', 'results', 'comment','refrences', 'test','results-detail'])
urlpatterns = patterns('',
       url(r'^$', query, name='list_blogs'),
       url(r'^result(\d+)/?$', show_result, name='blog_result'),
       url(r'^index$', blog_index, name='index'),
       url(r'^query/?$', query, name='query_blogs'),
       url(r'^collection/?$', blog_collection, name='blog_collection'),
       url(r'^(\d+)/(%s)?/?$' % blog_blocks, blog_detail, name='blog_detail'),
       url(r'^(?P<objid>\d+)/collect/?$',
           add_user_to_m2m,
           name='blog_collect',
           kwargs={'m2m':'collected_by', 'model': SciBlog}),
       url(r'^(?P<objid>\d+)/understand/?$',
           add_user_to_m2m,
           name='blog_understood',
           kwargs={'m2m':'catched_by', 'model': SciBlog}),
       url(r'^annotation/(?P<objid>\d+)/collect/?$',
           add_user_to_m2m,
           name='annotation_collect',
           kwargs={'m2m':'collected_by', 'model': BlogAnnotation}),
)

