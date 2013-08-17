# -*- coding: utf-8 -*-

"""
apps/indicator views

"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404
# CRSF
from django.template import RequestContext

# haystack search
from haystack.query import SearchQuerySet

from indicator import models as im
from indicator.forms import *
from indicator.tools import *

# apps/utils
from utils.search_tools import objects_of_sqs

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

    TODO:
    * when to recommend indicators
    * how to deal with non-standard units
    """
    template = 'indicator/SheetDefault.html'
    letters = map(chr, range(ord('a'), ord('z')+1))
    # indicators
    indicators = []
    followed_indicators = []
    r_indicators = []

    # get followed indicator, P[inyin] dict format
    followed_indicators_pdict = get_followed_indicator(request.user.id)
    # convert to list
    for l in letters:
        followed_indicators += followed_indicators_pdict[l]

    ## TODO: when to recommend indicators for user ??
    if not followed_indicators:
        # if no followed indicators yet, then recommend 2 indicators
        r_indicators_unsort = [
                im.Indicator.objects.get(id=ri['id']).dump()
                for ri in recommend_indicator(request.user.id, 2)
        ]
        r_indicators= sorted(r_indicators_unsort,
                key = lambda item: item['pinyin'])

    # recommended indicators behind followed ones
    indicators = followed_indicators + r_indicators

    # process 'indicators' list, to add following keys:         # {{{
    #   ref_text:
    #   ref_value:
    #   std_unit_symbol:
    #   record_empty: bool, if has no record, then True
    for ind in indicators:
        ind_obj = get_object_or_404(im.Indicator, id=ind['id'])
        # check if 'indicator.is_ready()'
        if not ind_obj.is_ready():
            raise ValueError(u"Indicator id=%s is NOT ready yet!"
                    % ind_obj.id)
        # the indicator is ready
        dataType = ind_obj.dataType
        confine = ind_obj.get_confine()
        ## set 'ref_text', 'ref_value', 'std_unit_*'
        if dataType in [ind_obj.FLOAT_TYPE, ind_obj.RANGE_TYPE,
                ind_obj.FLOAT_RANGE_TYPE]:
            ind['ref_text'] = u"参考范围"
            # ref_value
            human_max = confine.get('human_max')
            human_min = confine.get('human_min')
            ind['ref_value'] = format_data(ind_obj,
                    val_max=human_max, val_min=human_min)
            # set 'std_unit_*'
            ind['std_unit_name'] = confine.get('unit').get('name')
            ind['std_unit_symbol'] = confine.get('unit').get('symbol')
        elif dataType in [ind_obj.INTEGER_TYPE, ind_obj.PM_TYPE]:
            ind['ref_text'] = u"参考值"
            # ref_value
            val_norm = confine.get('val_norm')
            ind['ref_value'] = format_data(ind_obj, value=val_norm)
            # std_unit
            ind['std_unit_name'] = u""
            ind['std_unit_symbol'] = u""
        else:
            ind['ref_text'] = u"参考"
            ind['ref_value'] = None
            ind['std_unit_name'] = None
            ind['std_unit_symbol'] = None
        ## check record of indicator
        records = ind_obj.indicator_records.filter(user=request.user).\
                order_by('-date', '-updated_at')
        if records:
            ind['record_empty'] = False
            # last record of the indicator
            last_record = records[0]
            if dataType in [ind_obj.INTEGER_TYPE, ind_obj.PM_TYPE,
                    ind_obj.FLOAT_TYPE]:
                value_str = format_data(ind_obj, value=last_record.value)
            elif dataType == ind_obj.RANGE_TYPE:
                value_str = format_data(ind_obj,
                        val_max=last_record.val_max,
                        val_min=last_record.val_min)
            elif dataType == ind_obj.FLOAT_RANGE_TYPE:
                value = last_record.value
                val_max = last_record.val_max
                val_min = last_record.val_min
                if value is not None:
                    value_str = format_data(ind_obj, value=value)
                elif (val_max is not None) and (val_min is not None):
                    value_str = format_data(ind_obj,
                            val_max=val_max, val_min=val_min)
                else:
                    value_str = u''
            else:
                # unknow
                value_str = u''
            # save to dict
            ind['last_record'] = {
                'date': last_record.date.isoformat(),
                'value_str': value_str,
            }
        else:
            ind['record_empty'] = True
            ind['last_record'] = {}
    # }}}

    data = {
        'indicators': indicators,
    }
    # render template
    #raise ValueError
    return render(request, template, data)
# }}}


# indicator/NewDeleteIndex.html {{{
@login_required
def indicator_fanduf(request):
    """
    follow/unfollow indicator

    Note:
    * when 'page_condition == all',
      indicators -> indicators_pdict, in 'P[inyin] dict' format
    * other 'page_condition', 'indicators' a object list
    """
    template = 'indicator/NewDeleteIndex.html'
    letters = map(chr, range(ord('a'), ord('z')+1))

    # get 7 categories (page can only contains 1+7 categories)
    categories = im.IndicatorCategory.objects.all().\
            order_by('id')[:7]
    # set default value for 'selected_cat*'
    selected_catid = None
    selected_category = None
    # default parameters
    indicators = None
    search_kw_empty = False
    search_result_empty = False

    # get/post views
    if request.method == 'GET':
        # default page_condition: "all"
        selected_catid = "all"
        page_condition = "all"
        # page_condition: "category"
        # select category / search indicator
        if 'tab' in request.GET:
            # tab: selected category, default "all"
            selected_catid = request.GET.get('tab')
            if selected_catid == "all" or selected_catid == "":
                page_condition = "all"
            else:
                selected_catid = int(selected_catid)
                selected_category = get_object_or_404(
                        im.IndicatorCategory, id=selected_catid)
                page_condition = "category"
                # get indicators of the category
                indicators = selected_category.indicators.\
                        all().order_by('pinyin')
        # page_condition: "search"
        # can override the above 'category' if 'tab' & 'kw' both exist
        if 'kw' in request.GET:
            # kw: search keyword to find indicator
            search_kw = request.GET.get('kw')
            page_condition = "search"
            selected_catid = None
            # check search keyword
            if search_kw == "":
                search_kw_empty = True
            else:
                # search
                # TODO: howto order_by() by 'pinyin'
                sqs = SearchQuerySet().models(im.Indicator).\
                        filter(content=search_kw)
                if sqs:
                    # search result not empty
                    inds_unsort = [ind.dump()
                            for ind in objects_of_sqs(sqs)]
                    indicators = sorted(inds_unsort,
                            key = lambda item: item['pinyin'])
                else:
                    search_result_empty = True
    elif request.method == 'POST':
        # posted data of followed indicators
        # TODO
        post = request.POST
        raise ValueError(u"TODO")
    else:
        # XXX
        raise Http404

    # all indicators
    if page_condition == "all":
        # get indicators, P[inyin] dict format
        indicators = get_indicator()

    # get followed indicator, P[inyin] dict format
    followed_indicators_pdict = get_followed_indicator(request.user.id)
    # convert to list
    followed_indicators = []
    for l in letters:
        followed_indicators += followed_indicators_pdict[l]

    data = {
        'page_condition': page_condition,
        'categories': categories,
        'selected_category': selected_category,
        'selected_catid': selected_catid,
        'letters': letters,
        'indicators': indicators,
        'followed_indicators': followed_indicators,
        'search_kw_empty': search_kw_empty,
        'search_result_empty': search_result_empty,
    }
    # render page
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
    return render(request, template)
# }}}


# indicator/popup/EditHistoryData.html {{{
@login_required
def indicator_edithistorydata(request):
    """
    popup page to edit history data for an indicator
    """
    template = 'indicator/popup/EditHistoryData.html'
    return render(request, template)
# }}}


# indicator/popup/IndexDesc.html {{{
@login_required
def indicator_indexdesc(request):
    """
    description for an indicator
    """
    template = 'indicator/popup/IndexDesc.html'
    return render(request, template)
# }}}


###########################################################
###### ajax ######
# ajax_act_index {{{
@login_required
def ajax_act_index(request):
    """
    index action (add/minus)
    follow/unfollow indicator
    """
    # default 'fail'
    result = 'fail'
    #if request.is_ajax():
    if True:
        # check index_id -> indicator_id
        if request.GET.get('index_id') is not None:
            index_id = request.GET.get('index_id')
            try:
                indicator_id = int(index_id)
            except ValueError:
                print u'Error: Given index_id="%s" cannot convert to integer' % indicator_id
                result = 'fail'
                return HttpResponse(result)
        # check 'act': add/minus -> action: follow/unfollow
        if request.GET.get('act') is not None:
            action = request.GET.get('act')
            if action == "add":
                # follow
                if follow_indicator(request.user.id, indicator_id):
                    result = 'success'
            elif action == "minus":
                # unfollow
                if unfollow_indicator(request.user.id, indicator_id):
                    result = 'success'
            else:
                raise ValueError(u'Error: Given act="%s" unknown' % action)
                result = 'fail'

    return HttpResponse(result)
# }}}


# ajax_close_sub_title {{{
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
# }}}


# ajax_edit_history_data {{{
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
# }}}


# ajax_get_card_data_chart {{{
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
# }}}


# ajax_get_card_data_table {{{
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
# }}}


# ajax_unfollow_indicator {{{
@login_required
def ajax_unfollow_indicator(request):
    """
    respone to the ajax request from 'delete_card_tip.js'
    unfollow the specified indicator: GET.indicator_id
    """
    # default 'fail'
    result = 'fail'
    if request.is_ajax():
        if request.GET.get('indicator_id') is not None:
            indicator_id = request.GET.get('indicator_id')
            try:
                indicator_id = int(indicator_id)
            except ValueError:
                print u'Error: Given indicator_id="%s" cannot convert to integer' % indicator_id
                result = 'fail'
            if unfollow_indicator(request.user.id, indicator_id):
                result = 'success'

    # return result
    return HttpResponse(result)
# }}}


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
    for l in all_letters:
        followed_indicators += followed_indicators_pdict[l]

    list = []

    data = {
        'all_letters': all_letters,
        'all_indicators': all_indicators,
        'followed_indicators': followed_indicators,
        'list': list,
    }
    return render(request, template, data)

