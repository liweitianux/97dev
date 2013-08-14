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
        name='show_category'),
    # Indicator, name='show-indicator'
    url(r'^show/indicator/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=im.Indicator,
            template_name='show_indicator.html'),
        name='show_indicator'),
    ## IndicatorRecord, name='show-record'
    ## TODO: howto add '@login_required'
    #url(r'^show/record/(?P<pk>\d+)/$',
    #    DetailView.as_view(
    #        model=im.IndicatorRecord,
    #        template_name='show_record.html'),
    #    name='show_record'),
)

## UI pages
urlpatterns += patterns('',
    # indicator_index
    url(r'^$',
        direct_to_template, {'template': 'indicator/index.html'},
        name='indicator_index'),
    # indicator_sidebar
    url(r'^sidebar/$',
        direct_to_template, {'template': 'indicator/SideBar.html'},
        name='indicator_sidebar'),
    # indicator_status, 指标状态
    url(r'^status/$',
        direct_to_template, {'template': 'indicator/SheetDefault.html'},
        name='indicator_status'),
    # follow_indicator, 关注指标
    url(r'^follow/$',
        direct_to_template, {'template': 'indicator/NewDeleteIndex.html'},
        name='follow_indicator'),
    ## indicator: popup
    # DeleteCardTip
    url(r'^popup/deletecardtip/$',
        direct_to_template, {'template': 'indicator/popup/DeleteCardTip.html'},
        name='indicator_deletecardtip'),
    # EditHistoryData
    url(r'^popup/edithistorydata/$',
        direct_to_template, {'template': 'indicator/popup/EditHistoryData.html'},
        name='indicator_edithistorydata'),
    # IndexDesc
    url(r'^popup/indexdesc/$',
        direct_to_template, {'template': 'indicator/popup/IndexDesc.html'},
        name='indicator_indexdesc'),
)

## UI ajax
urlpatterns += patterns('indicator.views',
    # act_index
    # index action (add/minus): follow/unfollow indicator
    url(r'^ajax/act_index/$',
        'ajax_act_index',
        name='indicator_ajax_actindex'),
    # close_sub_title
    # close the small prompt banner above the indicator cards
    url(r'^ajax/close_sub_title/$',
        'ajax_close_sub_title',
        name='indicator_ajax_closesubtitle'),
    # edit_history_data
    url(r'^ajax/edit_history_data/$',
        'ajax_edit_history_data',
        name='indicator_ajax_edithistorydata'),
    # get_card_data_chart
    url(r'^ajax/get_card_data_chart/$',
        'ajax_get_card_data_chart',
        name='indicator_ajax_getcarddatachart'),
    # get_card_data_table
    url(r'^ajax/get_card_data_table/$',
        'ajax_get_card_data_table',
        name='indicator_ajax_getcarddatatable'),
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
    url(r'^done/$', direct_to_template, { 'template': 'indicator/done.html' }),
)

