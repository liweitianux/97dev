# -*- coding: utf-8 -*-

"""
URL configuration for apps/indicator
"""

from django.conf.urls.defaults import *

from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template

from indicator import models as im



## named URLs
## for 'django.core.urlresolvers.reverse()' in 'get_absolute_url()'
urlpatterns = patterns('indicator.views',
    # IndicatorCategory, name='show-category'
    url(r'^show/category/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=im.IndicatorCategory,
            template_name='show_category.html'),
        name='show-category'),
    # Indicator, name='show-indicator'
    url(r'^show/indicator/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=im.Indicator,
            template_name='show_indicator.html'),
        name='show-indicator'),
    # IndicatorRecord, name='show-record'
    # TODO: howto add '@login_required'
    url(r'^show/record/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=im.IndicatorRecord,
            template_name='show_record.html'),
        name='show-record'),
)


urlpatterns += patterns('indicator.views',
    ## test
    url(r'^test/$', 'test_view', name='test'),
    ## get_indicator_view
    url(r'^list/(?P<startswith>all)/$',
        'get_indicator_view', name='get_indicator_view'),
    url(r'^list/(?P<startswith>[a-zA-Z]+)/$',
        'get_indicator_view', name='get_indicator_view'),
    url(r'^category/(?P<category_id>all)/$',
        'get_indicator_view', name='get_indicator_view'),
    url(r'^category/(?P<category_id>\d+)/$',
        'get_indicator_view', name='get_indicator_view'),
    url(r'^category/(?P<category_id>all)/(?P<startswith>all)/$',
        'get_indicator_view', name='get_indicator_view'),
    url(r'^category/(?P<category_id>\d+)/(?P<startswith>all)/$',
        'get_indicator_view', name='get_indicator_view'),
    url(r'^category/(?P<category_id>all)/(?P<startswith>[a-zA-Z]+)/$',
        'get_indicator_view', name='get_indicator_view'),
    url(r'^category/(?P<category_id>\d+)/(?P<startswith>[a-zA-Z]+)/$',
        'get_indicator_view', name='get_indicator_view'),
    ## get_followed_indicator_view
    url(r'^followed/(?P<startswith>all)/$',
        'get_followed_indicator_view', name='get_followed_indicator_view'),
    url(r'^followed/(?P<startswith>[a-zA-Z]+)/$',
        'get_followed_indicator_view', name='get_followed_indicator_view'),
    url(r'^followed/category/(?P<category_id>all)/$',
        'get_followed_indicator_view', name='get_followed_indicator_view'),
    url(r'^followed/category/(?P<category_id>\d+)/$',
        'get_followed_indicator_view', name='get_followed_indicator_view'),
    ## get_unfollowed_indicator_view
    url(r'^unfollowed/(?P<startswith>all)/$',
        'get_unfollowed_indicator_view', name='get_unfollowed_indicator_view'),
    url(r'^unfollowed/(?P<startswith>[a-zA-Z]+)/$',
        'get_unfollowed_indicator_view', name='get_unfollowed_indicator_view'),
    url(r'^unfollowed/category/(?P<category_id>all)/$',
        'get_unfollowed_indicator_view', name='get_unfollowed_indicator_view'),
    url(r'^unfollowed/category/(?P<category_id>\d+)/$',
        'get_unfollowed_indicator_view', name='get_unfollowed_indicator_view'),
    ## get_record view
    url(r'^record/(?P<indicator_id>\d+)/(?P<date_range>\d{8}-\d{8})/$',
        'get_record_view', name='get_record_view'),
    url(r'^record/(?P<indicator_id>\d+)/(?P<date_range>\d{8}-\d{8})/std/$',
        'get_record_view', { 'std': True }),
    ## recommend indicator
    url(r'^recommend/indicator/(?P<number>\d+)/$',
        'recommend_indicator_view', name='recommend_indicator'),
    ## add/edit category
    url(r'^add/category/$', 'add_edit_category',
        name='add_category'),
    url(r'^edit/category/(?P<category_id>\d+)/$', 'add_edit_category',
        name='edit_category'),
    ## add/edit indicator
    url(r'^add/indicator/$', 'add_edit_indicator',
        name='add_indicator'),
    url(r'^edit/indicator/(?P<indicator_id>\d+)/$', 'add_edit_indicator',
        name='edit_indicator'),
    ## add/edit unit
    url(r'^add/unit/$', 'add_edit_unit',
        name='add_unit'),
    url(r'^edit/unit/(?P<unit_id>\d+)/$', 'add_edit_unit',
        name='edit_unit'),
    ## add/edit innateconfine
    url(r'^add/confine/$', 'add_edit_confine',
        name='add_confine'),
    url(r'^edit/confine/(?P<confine_id>\d+)/$', 'add_edit_confine',
        name='edit_confine'),
    ## add/edit record
    url(r'^add/record/$', 'add_edit_record',
        name='add_record'),
    url(r'^edit/record/(?P<record_id>\d+)/$', 'add_edit_record',
        name='edit_record'),
    ## add record history (modify history NOT allowed)
    url(r'^add/recordhistory/$', 'add_recordhistory',
        name='add_recordhistory'),
    url(r'^add/recordhistory/(?P<record_id>\d+)/$', 'add_recordhistory',
        name='add_recordhistory'),
)


urlpatterns += patterns('',
    ## done
    url(r'^done/$', direct_to_template, { 'template': 'done.html' }),
)

