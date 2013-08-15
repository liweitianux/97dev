# -*- coding: utf-8 -*-

"""
apps/indicator views

"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404
# CRSF
from django.template import RequestContext

from indicator import models as im
from indicator.forms import *
from indicator.tools import *

import re
import datetime

## json
# Django 1.5 deprecates 'django.utils.simplejson'
# in favor of Python 2.6's bulti-in 'json' module
try:
    import json
except ImportError:
    from django.utils import simplejson as json



def get_indicator_view(request, **kwargs):
    idict = get_indicator(**kwargs)
    return HttpResponse("%s" % idict)


@login_required
def get_followed_indicator_view(request, **kwargs):
    idict = get_followed_indicator(request.user.id, **kwargs)
    return HttpResponse("%s" % idict)


@login_required
def get_unfollowed_indicator_view(request, **kwargs):
    idict = get_unfollowed_indicator(request.user.id, **kwargs)
    return HttpResponse("%s" % idict)


@login_required
def recommend_indicator_view(request, **kwargs):
    ilist = recommend_indicator(request.user.id, **kwargs)
    return HttpResponse("%s" % ilist)


# follow_indicator {{{
@login_required
def follow_indicator(request, indicator_id):
    """
    用户关注指标
    """
    try:
        indicator = im.Indicator.objects.get(pk=int(indicator_id))
        ui, created = im.UserIndicator.objects.get_or_create(
                user=request.user)
        ui.followedIndicators.add(indicator)
        return { 'success': True }
    except:
        return { 'success': False }
# }}}


# unfollow_indicator {{{
@login_required
def unfollow_indicator(request, indicator_id):
    """
    用户取消关注指标
    """
    try:
        indicator = im.Indicator.objects.get(pk=int(indicator_id))
        ui, created = im.UserIndicator.objects.get_or_create(
                user=request.user)
        ui.followedIndicators.remove(indicator)
        return { 'success': True }
    except:
        return { 'success': False }
# }}}


# get_record_view {{{
@login_required
def get_record_view(request, indicator_id, date_range, **kwargs):
    """
    get IndicatorRecord record
    """
    indicator_id = int(indicator_id)
    # regex to match given 'date_range' (yyyymmdd-yyyymmdd)
    p = re.compile(r'^(?P<b_y>\d{4})(?P<b_m>\d{2})(?P<b_d>\d{2})-(?P<e_y>\d{4})(?P<e_m>\d{2})(?P<e_d>\d{2})$')
    m = p.match(date_range)
    # begin date
    begin_y = int(m.group('b_y'))
    # remove '^0'; avoid the '0???' octal number
    begin_m = int(re.sub(r'^0', '', m.group('b_m')))
    begin_d = int(re.sub(r'^0', '', m.group('b_d')))
    # end date
    end_y = int(m.group('b_y'))
    end_m = int(re.sub(r'^0', '', m.group('e_m')))
    end_d = int(re.sub(r'^0', '', m.group('e_d')))
    # date
    begin = datetime.date(begin_y, begin_m, begin_d)
    end = datetime.date(end_y, end_m, end_d)
    data = get_record(request.user.id, indicator_id=indicator_id,
            begin=begin, end=end, **kwargs)
    return HttpResponse("%s" % data)
# }}}



###########################################################
###### forms ######

## add_edit_category                                        # {{{
@login_required
def add_edit_category(request, category_id=None, template='indicator/simple.html'):
    """
    add/edit category: 'models.IndicatorCategory'
    for 'staff' or 'normal user'
    """
    # get or create model instance
    if category_id:
        category_id = int(category_id)
        category = get_object_or_404(im.IndicatorCategory,
                id=category_id)
        action = 'Edit'
        # check the user
        # 'staff' can edit all data;
        # normal users can only edit their own.
        if category.addByUser != request.user and (
                not request.user.is_staff):
            return HttpResponseForbidden()
    else:
        category = im.IndicatorCategory(addByUser=request.user)
        action = 'Add'

    if request.method == 'POST':
        form = IndicatorCategoryForm(request.POST, instance=category)
        if form.is_valid():
            # form posted and valid
            # save form to create/update the model instance
            form.save()
            # redirect url, avoid page reload/refresh
            return HttpResponseRedirect('/indicator/done/')
    else:
        # form with data of the specified instance
        form = IndicatorCategoryForm(instance=category)

    return render(request, template, {
        'object': 'IndicatorCategory',
        'action': action,
        'form': form,
    })
# }}}


# add_edit_indicator                                        # {{{
@login_required
def add_edit_indicator(request, indicator_id=None, template='indicator/simple.html'):
    """
    add/edit indicator: 'models.Indicator'
    for 'staff' or 'normal user'
    """
    if indicator_id:
        indicator_id = int(indicator_id)
        indicator = get_object_or_404(im.Indicator,
                id=indicator_id)
        action = 'Edit'
        # check the user
        # 'staff' can edit all data;
        # normal users can only edit their own.
        if indicator.addByUser != request.user and (
                not request.user.is_staff):
            return HttpResponseForbidden()
    else:
        indicator = im.Indicator(addByUser=request.user)
        action = 'Add'

    if request.method == 'POST':
        form = IndicatorForm(request.POST, instance=indicator)
        if form.is_valid():
            # form posted and valid
            form.save()
            # redirect url, avoid page reload/refresh
            return HttpResponseRedirect('/indicator/done/')
    else:
        # form with instance
        form = IndicatorForm(instance=indicator)

    return render(request, template, {
        'object': 'Indicator',
        'action': action,
        'form': form,
    })
# }}}


## add_edit_unit {{{
@login_required
def add_edit_unit(request, unit_id=None, template='indicator/simple.html'):
    """
    add unit for indicator
    """
    if unit_id:
        unit_id = int(unit_id)
        unit = get_object_or_404(im.Unit, id=unit_id)
        action = 'Edit'
        # check the user
        # 'staff' can edit all data;
        # normal users can only edit their own.
        if unit.addByUser != request.user and (
                not request.user.is_staff):
            return HttpResponseForbidden()
    else:
        unit = im.Unit(addByUser=request.user)
        action = 'Add'

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            # form posted and valid
            form.save()
            # redirect url, avoid page reload/refresh
            return HttpResponseRedirect('/indicator/done/')
    else:
        # form with instance
        form = UnitForm(instance=unit)

    return render(request, template, {
        'object': 'Unit',
        'action': action,
        'form': form,
    })
# }}}


## add_edit_confine {{{
@login_required
def add_edit_confine(request, confine_id=None, template='indicator/simple.html'):
    """
    InnateConfine
    add confines for indicator
    """
    if confine_id:
        confine_id = int(confine_id)
        confine = get_object_or_404(im.InnateConfine, id=confine_id)
        action = 'Edit'
        # check the user
        # 'staff' can edit all data;
        # normal users can only edit their own.
        if confine.addByUser != request.user and (
                not request.user.is_staff):
            return HttpResponseForbidden()
    else:
        confine = im.InnateConfine(addByUser=request.user)
        action = 'Add'

    if request.method == 'POST':
        form = InnateConfineForm(request.POST, instance=confine)
        if form.is_valid():
            # form posted and valid
            form.save()
            # redirect url, avoid page reload/refresh
            return HttpResponseRedirect('/indicator/done/')
    else:
        # form with instance
        form = InnateConfineForm(instance=confine)

    return render(request, template, {
        'object': 'InnateConfine',
        'action': action,
        'form': form,
    })
# }}}


## add_edit_record {{{
@login_required
def add_edit_record(request, record_id=None, template='indicator/simple.html'):
    """
    add/edit 'IndicatorRecord'

    staff 能自由地修改所有的记录，并且无需填写"修改原因"；
    普通用户只能修改自己的记录，而且必须填写"修改原因" -> RecordHistory

    TODO:
    * 当用户选择好"indicator"后，重新筛选"unit"，只提供与"indicator"
      对应的"unit"供选择；
    * 对"普通用户"增加限制，修改数据"记录"时必须同时提交"修改原因"，
      对应模型"RecordHistory"。
    """
    if record_id:
        record_id = int(record_id)
        record = get_object_or_404(im.IndicatorRecord, id=record_id)
        action = 'Edit'
        # check the user
        if request.user.is_staff:
            # 'staff' can edit all data;
            pass
        elif request.user == record.user:
            # user modify the record
            return HttpResponse("Not finished yet ...")
            #return modify_record(request, record_id)
        else:
            return HttpResponseForbidden()
    else:
        record = im.IndicatorRecord(user=request.user)
        action = 'Add'

    if request.method == 'POST':
        form = IndicatorRecordForm(request.POST, instance=record)
        if form.is_valid():
            #raise ValueError
            form.save()
            # redirect url, avoid page reload/refresh
            return HttpResponseRedirect('/indicator/done/')
    else:
        # form with instance
        form = IndicatorRecordForm(instance=record)

    return render(request, template, {
        'object': 'IndicatorRecord',
        'action': action,
        'form': form,
    })
# }}}


## modify_record {{{
@login_required
def modify_record(request, record_id=None, template='indicator/simple.html'):
    """
    modify an existing IndicatorRecord

    TODO:
    a new 'RecordHistory' is added to record the modification reason
    and backup the original data
    """
    if record_id:
        record_id = int(record_id)
        record = get_object_or_404(im.IndicatorRecord, id=record_id)
        action = 'Edit'
        # check the user
        if request.user.is_staff:
            # 'staff' can edit all data;
            return add_edit_record(request, record_id)
        elif request.user == record.user:
            # user modify the record
            action = 'Modify'
            pass
        else:
            return HttpResponseForbidden()
    else:
        return add_edit_record(request)

    if request.method == 'POST':
        form = IndicatorRecordForm(request.POST, instance=record)
        if form.is_valid():
            # form posted and valid
            # TODO
            raise ValueError(u"该功能尚未完整实现")
            form.save()
            # redirect url, avoid page reload/refresh
            return HttpResponseRedirect('/indicator/done/')
    else:
        # form with instance
        form = IndicatorRecordForm(instance=record)

    return render(request, template, {
        'object': 'IndicatorRecord',
        'action': action,
        'form': form,
    })
## }}}


## add_recordhistory {{{
@login_required
def add_recordhistory(request, record_id, template='indicator/simple.html'):
    """
    add 'RecordHistory' for a record by given

    'staff' should use the 'admin' interface.
    """
    record_id = int(record_id)
    record = get_object_or_404(im.IndicatorRecord, id=record_id)
    recordhistory = im.RecordHistory(indicatorRecord=record)
    action = 'Add'
    # check the user
    if request.user != record.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = RecordHistoryForm(request.POST, instance=recordhistory)
        if form.is_valid():
            # form posted and valid
            form.save()
            # redirect url, avoid page reload/refresh
            return HttpResponseRedirect('/indicator/done/')
    else:
        # form with instance
        form = RecordHistoryForm(instance=recordhistory)

    return render(request, template, {
        'object': 'RecordHistory',
        'action': action,
        'form': form,
    })
# }}}


###########################################################
###### indicator UI pages ######
# indicator/index.html {{{
@login_required
def indicator_index(request):
    """
    index page for indicator
    """
    template = 'indicator/index.html'
    return render(request, template)
# }}}


# indicator/SideBar.html {{{
@login_required
def indicator_sidebar(request):
    """
    sidebar page for indicator
    """
    template = 'indicator/SideBar.html'
    return render(request, template)
# }}}


# indicator/SheetDefault.html {{{
@login_required
def indicator_status(request):
    """
    status page for indicator
    add/edit/view indicator data
    """
    template = 'indicator/SheetDefault.html'
    return render(request, template)
# }}}


# indicator/NewDeleteIndex.html {{{
@login_required
def follow_indicator(request):
    """
    follow/unfollow indicator
    """
    template = 'indicator/NewDeleteIndex.html'
    letters = map(chr, range(ord('a'), ord('z')+1))

    # get 7 categories (page can only contains 1+7 categories)
    categories = im.IndicatorCategory.objects.all().\
            order_by('id')[:7]
    # get indicators, P[inyin] dict format
    indicators_pdict = get_indicator()
    # get followed indicator, P[inyin] dict format
    followed_indicators_pdict = get_followed_indicator(request.user.id)
    # convert to list
    followed_indicators = []
    for l in letters:
        followed_indicators += followed_indicators_pdict[l]

    # selected category, default "all"
    if request.GET.get('tab'):
        selected_catid = request.GET.get('tab')
        if selected_catid != "all":
            selected_catid = int(selected_catid)
    else:
        selected_catid = "all"

    data = {
        'categories': categories,
        'selected_catid': selected_catid,
        'letters': letters,
        'indicators_pdict': indicators_pdict,
        'followed_indicators': followed_indicators,
    }

    return render(request, template, data)
# }}}


## popup pages
# indicator/popup/DeleteCardTip.html {{{
@login_required
def indicator_deletecardtip(request):
    """
    prompted tip for deleting a card
    """
    template = 'indicator/popup/DeleteCardTip.html'
    return render_to_response(template)
# }}}


# indicator/popup/EditHistoryData.html {{{
@login_required
def indicator_edithistorydata(request):
    """
    popup page to edit history data for an indicator
    """
    template = 'indicator/popup/EditHistoryData.html'
    return render_to_response(template)
# }}}


# indicator/popup/IndexDesc.html {{{
@login_required
def indicator_indexdesc(request):
    """
    description for an indicator
    """
    template = 'indicator/popup/IndexDesc.html'
    return render_to_response(template)
# }}}


###########################################################
###### ajax ######
@login_required
def ajax_act_index(request):
    """
    index action (add/minus)
    follow/unfollow indicator

    TODO:
    * howto relate 'index_id' to 'indicator_id'?
    * howto implement follow/unfollow indicator function?
    """
    if request.is_ajax():
        result = 'success'
    else:
        result = 'fail'
        #raise Http404
    return HttpResponse(result)


def ajax_close_sub_title(request):
    """
    close the small prompt banner above the indicator cards

    'indicator/static/javascripts/sheetdefault.js'
    """
    if request.is_ajax():
        result = 'success'
    else:
        result = 'fail'
        #raise Http404
    return HttpResponse(result)


@login_required
def ajax_edit_history_data(request):
    """
    edit history data
    used in 'detail history' view card
    """
    if request.is_ajax():
        result = 'success'
    else:
        result = 'fail'
        #raise Http404
    return HttpResponse(result)


@login_required
def ajax_get_card_data_chart(request):
    """
    'indicator/static/javascripts/load_card.js'
    get card data
    for the 'chart' within the card
    format: [v1, v2, v3, ...]

    NB.
    每一天都要有数据，否则时间轴对不上 (load_card.js: redraw_chard())
    TODO:
    workaround for the above problem!
    """
    # TODO
    if request.is_ajax():
        result = [6.0, 5.9, 5.5, 4.5, 6.2, 6.5, 5.2, 6.0,
                  5.9, 5.5, 4.5, 6.2, 6.5, 5.2, 6.0, 5.9,
                  5.5, 4.5, 6.2, 6.5]
    else:
        result = ''
        #raise Http404
    return HttpResponse(json.dumps(result),
            mimetype='application/json')


@login_required
def ajax_get_card_data_table(request):
    """
    get card data
    for used in 'detail data card'
    format:
    <tr><td>yyyy-mm-dd</td><td>hh:mm</td><td>value unit</td></tr>
    """
    # TODO
    if request.is_ajax():
        result = """
            <tr><td>2013-08-10</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-09</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-08</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-08</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-07</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-06</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-05</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-04</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-03</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-02</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-08-01</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-07-31</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            <tr><td>2013-07-30</td><td>11:20</td><td>100x10^4拷贝/mL</td></tr>
            """
    else:
        result = ''
        #raise Http404
    return HttpResponse(result)


###########################################################

### test_view ###
def test_view(request, **kwargs):
    """
    test view
    'indicator/templates/indicator/test.html'
    """
    template = 'indicator/test.html'
    all_letters = map(chr, range(ord('a'), ord('z')+1))
    all_indicators = get_indicator()
    followed_indicators_pdict = get_followed_indicator(request.user.id)
    # convert to list
    followed_indicators = []
    for l in letters:
        followed_indicators += followed_indicators_pdict[l]

    data = {
        'all_letters': all_letters,
        'all_indicators': all_indicators,
        'followed_indicators': followed_indicators,
    }
    return render(request, template, data)

