# -*- coding: utf-8 -*-

"""
apps/indicator views

"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
# CRSF
from django.template import RequestContext

# haystack search
from haystack.query import SearchQuerySet

from indicator import models as im
from indicator.forms import *
from indicator.tools import *

from sciblog import models as sm

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


## add_recordhistory_view {{{
@login_required
def add_recordhistory_view(request, record_id, template='indicator/simple.html'):
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
    * how to deal with non-standard units
    """
    # period between two recommendation of indicators (default 40 days)
    recommend_period = 40
    #
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
    # add key 'recommended', False
    for ind in followed_indicators:
        ind['recommended'] = False

    ## XXX: recommend indicators for user {{{
    now_utc = datetime.datetime.utcnow().replace(tzinfo=utc)
    ui, created = im.UserIndicator.objects.get_or_create(
            user=request.user)
    ui.save()
    # lastRecommendTime
    if ui.lastRecommendTime:
        td_lastrecommend = now_utc - ui.lastRecommendTime
    else:
        td_lastrecommend = None
    # sciblog.models.UserCollection
    uc, created = sm.UserCollection.objects.get_or_create(
            user=request.user)
    uc.save()
    # lastCollectAnnotationTime
    if uc.lastCollectAnnotationTime:
        td_lastcollectannotation = (uc.lastCollectAnnotationTime
                - ui.lastRecommendTime)
    else:
        td_lastcollectannotation = None
    # lastCatchBlogTime
    if uc.lastCatchBlogTime:
        td_lastcatchblog = uc.lastCatchBlogTime - ui.lastRecommendTime
    else:
        td_lastcatchblog = None
    # lastCollectBlogTime
    if uc.lastCollectBlogTime:
        td_lastcollectblog = uc.lastCollectBlogTime - ui.lastRecommendTime
    else:
        td_lastcollectblog = None
    ##
    if not followed_indicators:
        # if no followed indicators yet, then recommend 2 indicators
        r_indicators_unsort = [
                im.Indicator.objects.get(id=ri['id']).dump()
                for ri in recommend_indicator(request.user.id,
                    number=2, auto_follow=True)
        ]
    elif (td_lastrecommend is not None and \
            td_lastrecommend.days > recommend_period):
        # excess the 'recommend_period'
        r_indicators_unsort = [
                im.Indicator.objects.get(id=ri['id']).dump()
                for ri in recommend_indicator(request.user.id,
                    number=1, auto_follow=True)
        ]
    elif (     (td_lastcollectannotation is not None and \
                td_lastcollectannotation.total_seconds() > 0) \
            or (td_lastcatchblog is not None and \
                td_lastcatchblog.total_seconds() > 0) \
            or (td_lastcollectblog is not None and \
                td_lastcollectblog.total_seconds() > 0) ):
        # user has new collections
        # TODO: to improve the relations between recommended indicators
        #       with the user's new collections
        r_indicators_unsort = [
                im.Indicator.objects.get(id=ri['id']).dump()
                for ri in recommend_indicator(request.user.id,
                    number=1, auto_follow=True)
        ]
    else:
        # no recommendation
        r_indicators_unsort = []
    # sort (empty list OK)
    r_indicators= sorted(r_indicators_unsort,
            key = lambda item: item['pinyin'])
    # add key 'recommended', True
    for ind in r_indicators:
        ind['recommended'] = True
    # }}}

    # recommended indicators come first
    indicators = r_indicators + followed_indicators

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
            math_max = confine.get('math_max')
            math_min = confine.get('math_min')
            ind['ref_value'] = format_data(ind_obj,
                    val_max=human_max, val_min=human_min, type="html")
            ind['math_range_html'] = format_data(ind_obj,
                    val_max=math_max, val_min=math_min, type="html")
            # set 'std_unit_*'
            ind['std_unit_name'] = confine.get('unit').get('name')
            ind['std_unit_symbol'] = confine.get('unit').get('symbol')
        elif dataType in [ind_obj.INTEGER_TYPE, ind_obj.PM_TYPE]:
            ind['ref_text'] = u"参考值"
            # ref_value
            val_norm = confine.get('val_norm')
            ind['ref_value'] = format_data(ind_obj, value=val_norm,
                    type="html")
            ind['math_range_html'] = None
            # std_unit
            ind['std_unit_name'] = u""
            ind['std_unit_symbol'] = u""
        else:
            ind['ref_text'] = u"参考"
            ind['ref_value'] = None
            ind['math_range_html'] = None
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
                value_html = format_data(ind_obj,
                        value=last_record.value, type="html")
            elif dataType == ind_obj.RANGE_TYPE:
                value_html = format_data(ind_obj,
                        val_max=last_record.val_max,
                        val_min=last_record.val_min,
                        type="html")
            elif dataType == ind_obj.FLOAT_RANGE_TYPE:
                value = last_record.value
                val_max = last_record.val_max
                val_min = last_record.val_min
                if value is not None:
                    value_html = format_data(ind_obj, value=value,
                            type="html")
                elif (val_max is not None) and (val_min is not None):
                    value_html = format_data(ind_obj,
                            val_max=val_max, val_min=val_min,
                            type="html")
                else:
                    value_html = None
            else:
                # unknow
                value_html = None
            # save to dict
            ind['last_record'] = {
                'date': last_record.date.isoformat(),
                'value_html': value_html,
            }
        else:
            ind['record_empty'] = True
            ind['last_record'] = {}
    # }}}

    # dataType
    DATA_TYPES = {
        'INTEGER_TYPE': im.Indicator.INTEGER_TYPE,
        'FLOAT_TYPE': im.Indicator.FLOAT_TYPE,
        'RANGE_TYPE': im.Indicator.RANGE_TYPE,
        'FLOAT_RANGE_TYPE': im.Indicator.FLOAT_RANGE_TYPE,
        'PM_TYPE': im.Indicator.PM_TYPE,
    }
    # datatypes of indicators (for js)
    datatypes = {}
    # recordempty for indicators (for js)
    recordempty = {}
    # records of indicators (for js)
    confines = {}
    for ind in indicators:
        id = ind['id']
        ind_obj = get_object_or_404(im.Indicator, id=ind['id'])
        datatypes['id%d'%id] = ind_obj.dataType
        # recordempty
        recordempty['id%d'%id] = ind['record_empty']
        # confines
        confine = ind_obj.get_confine()
        confines['id%d'%id] = {
            'human_min': confine.get('human_min'),
            'human_max': confine.get('human_max'),
            'math_min': confine.get('math_min'),
            'math_max': confine.get('math_max'),
            'val_norm': confine.get('val_norm'),
            'math_range_html': ind['math_range_html'],
        }

    #print "indicators: ", indicators
    data = {
        'indicators': indicators,
        'DATA_TYPES': DATA_TYPES,
        'DATA_TYPES_json': json.dumps(DATA_TYPES),
        'datatypes_json': json.dumps(datatypes),
        'recordempty_json': json.dumps(recordempty),
        'confines_json': json.dumps(confines),
    }
    # render template
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
    # check 'card_id' -> indicator_id
    if request.GET.get('card_id') is not None:
        card_id = request.GET.get('card_id')
        try:
            indicator_id = int(card_id)
            ind_obj = im.Indicator.objects.get(id=indicator_id)
        except ValueError:
            print u'Error: Given card_id="%s" cannot convert to integer' % card_id
            raise Http404
        except im.Indicator.DoesNotExist:
            print u'Error: Indicator id="%s" NOT exist' % indicator_id
            raise Http404
    else:
        print u'Error: No card_id provided'
        raise Http404
    # check record 'date'
    if request.GET.get('date'):
        # 'date' given and not empty
        date = request.GET.get('date')
        try:
            datetime_in = datetime.datetime.strptime(date, '%Y-%m-%d')
            record_date = datetime_in.date()
        except ValueError:
            print u'Error: Given date="%s" invalid' % date
            raise Http404
    else:
        print u'Error: "date" not given or empty'
        raise Http404

    # get indicator record
    try:
        record_obj = im.IndicatorRecord.objects.get(
                indicator=ind_obj, date=record_date)
    except im.IndicatorRecord.DoesNotExist:
        print u'Error: no matching IndicatorRecord found'
        raise Http404
    except im.IndicatorRecord.MultipleObjectsReturned:
        print u'Error: multiple matching IndicatorRecord found'
        raise Http404

    # process indicator and record data
    # generate 'indicator_dict' and 'record_dict'           # {{{
    # check if 'indicator.is_ready()'
    if not ind_obj.is_ready():
        print u"Indicator id=%s is NOT ready yet!" % ind_obj.id
    # the indicator is ready
    dataType = ind_obj.dataType
    # confine
    confine = ind_obj.get_confine()
    confine_val_norm = confine.get('val_norm')
    confine_human_min = confine.get('human_min')
    confine_human_max = confine.get('human_max')
    confine_math_min = confine.get('math_min')
    confine_math_max = confine.get('math_max')
    std_unit_name = confine.get('unit').get('name')
    std_unit_symbol = confine.get('unit').get('symbol')
    # record data
    record_data_std = record_obj.get_data_std()
    record_value = record_data_std['value']
    record_val_min = record_data_std['val_min']
    record_val_max = record_data_std['val_max']
    record_unit_name = record_data_std.get('unit').get('name')
    record_unit_symbol = record_data_std.get('unit').get('symbol')
    record_is_normal = record_obj.is_normal()
    # check dataType
    if dataType == im.Indicator.INTEGER_TYPE:
        ref_text = u"参考值"
        ref_value = format_data(ind_obj, value=confine_val_norm,
                type="html")
        confine_math_range_html = None
        # TODO
        record_value_html = format_data(ind_obj, value=record_value,
                type="html")
        record_value_text = format_data(ind_obj, value=record_value,
                type="text")
    elif dataType == im.Indicator.FLOAT_TYPE:
        ref_text = u"参考范围"
        ref_value = format_data(ind_obj, val_max=confine_human_max,
                val_min=confine_human_min, type="html")
        confine_math_range_html = format_data(ind_obj,
                val_max=confine_math_max,
                val_min=confine_math_min, type="html")
        record_value_html = format_data(ind_obj, value=record_value,
                type="html")
        record_value_text = format_data(ind_obj, value=record_value,
                type="text")
    elif dataType == im.Indicator.RANGE_TYPE:
        ref_text = u"参考范围"
        ref_value = format_data(ind_obj, val_max=confine_human_max,
                val_min=confine_human_min, type="html")
        confine_math_range_html = format_data(ind_obj,
                val_max=confine_math_max,
                val_min=confine_math_min, type="html")
        record_value_html = format_data(ind_obj,
                val_min=record_val_min, val_max=record_val_max,
                type="html")
        record_value_text = format_data(ind_obj,
                val_min=record_val_min, val_max=record_val_max,
                type="text")
    elif dataType == im.Indicator.FLOAT_RANGE_TYPE:
        ref_text = u"参考范围"
        ref_value = format_data(ind_obj, val_max=confine_human_max,
                val_min=confine_human_min, type="html")
        confine_math_range_html = format_data(ind_obj,
                val_max=confine_math_max,
                val_min=confine_math_min, type="html")
        # TODO
        record_value_html = u"TODO"
        record_value_text = u"TODO"
    elif dataType == im.Indicator.PM_TYPE:
        ref_text = u"参考值"
        ref_value = format_data(ind_obj, value=confine_val_norm,
                type="html")
        confine_math_range_html = None
        record_value_html = format_data(ind_obj, value=record_value,
                type="html")
        record_value_text = format_data(ind_obj, value=record_value,
                type="text")
    else:
        ref_text = u"参考"
        ref_value = None
        confine_math_range_html = None
        std_unit_name = None
        std_unit_symbol = None
        record_value_html = None
        record_value_text = None
    # }}}

    # template data
    confine_dict = {
        'human_min': confine_human_min,
        'human_max': confine_human_max,
        'math_min': confine_math_min,
        'math_max': confine_math_max,
        'val_norm': confine_val_norm,
        'math_range_html': confine_math_range_html,
    }
    ind_dict = {
        'ref_text': ref_text,
        'ref_value': ref_value,
        'std_unit_name': std_unit_name,
        'std_unit_symbol': std_unit_symbol,
    }
    record_dict = {
        'date': record_date.isoformat(),
        'value_html': record_value_html,
        'value_text': record_value_text,
        'value': record_value,
        'val_min': record_val_min,
        'val_max': record_val_max,
        'unit_name': record_unit_name,
        'unit_symbol': record_unit_symbol,
        'is_normal': record_is_normal,
    }
    data = {
        'confine_dict': confine_dict,
        'confine_json': json.dumps(confine_dict),
        'indicator_obj': ind_obj,
        'indicator_dict': ind_dict,
        'record_obj': record_obj,
        'record_dict': record_dict,
        'record_json': json.dumps(record_dict),
    }
    #
    return render(request, template, data)
# }}}


# indicator/popup/IndexDesc.html {{{
@login_required
def indicator_indexdesc(request):
    """
    description for an indicator
    """
    template = 'indicator/popup/IndexDesc.html'
    # default parameters
    annotation = None
    annotation_not_found = False
    annotation_url = 'javascript:void(0)'
    collected_times = 0
    is_collected = False
    # check card_id -> indicator_id
    if request.GET.get('card_id') is not None:
        card_id = request.GET.get('card_id')
        try:
            indicator_id = int(card_id)
            ind_obj = im.Indicator.objects.get(id=indicator_id)
        except ValueError:
            print u'Error: Given card_id="%s" cannot convert to integer' % card_id
            raise Http404
        except im.Indicator.DoesNotExist:
            print u'Error: Indicator id="%s" NOT exist' % indicator_id
            raise Http404
    else:
        print u'Error: No card_id provided'
        raise Http404
    # get related 'BlogAnnotation', only type 'PROPER_NAME'
    related_annotations = ind_obj.related_indicators.\
            filter(objectType=im.RelatedIndicator.ANNOTATION_TYPE).\
            filter(annotation__type=sm.BlogAnnotation.PROPER_NOUN).\
            order_by('-weight')
    if related_annotations:
        # has related annotations
        annotation = related_annotations[0].annotation
        collected_times = len(annotation.collected_by.all())
        is_collected = annotation.is_collected_by(request.user)
        # TODO
        #annotation_url = annotation.get_absolute_url()
    else:
        annotation_not_found = True

    data = {
        'annotation_not_found': annotation_not_found,
        'annotation': annotation,
        'annotation_url': annotation_url,
        'collected_times': collected_times,
        'is_collected': is_collected,
        'indicator': ind_obj,
    }
    return render(request, template, data)
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
    if request.is_ajax():
        # check index_id -> indicator_id
        if request.GET.get('index_id') is not None:
            index_id = request.GET.get('index_id')
            try:
                indicator_id = int(index_id)
            except ValueError:
                print u'Error: Given index_id="%s" cannot convert to integer' % index_id
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


# ajax_add_record {{{
@login_required
def ajax_add_record(request):
    """
    add new record for given indicator using the POSTed data
    if the given date already has record, then return False

    error_code & error_string:
      1: unknown
     10: indicator_id
     20: record_exist
     30: record_invalid
    """
    data = {'failed': True, 'error_code': 1, 'error_string': 'unknown'}
    if request.is_ajax() and request.method == 'POST':
        #print request.POST.dict()
        indicator_id = request.POST.get('indicator_id')
        date_str = request.POST.get('date')
        value = request.POST.get('value')
        val_min_str = request.POST.get('val_min')
        val_max_str = request.POST.get('val_max')
        # get indicator object
        try:
            indicator_id = int(indicator_id)
            indicator_obj = get_object_or_404(im.Indicator,
                    id=indicator_id)
        except ValueError:
            data = {
                'failed': True,
                'error_code': 10,
                'error_string': 'indicator_id'
            }
            return HttpResponse(json.dumps(data),
                    mimetype='application/json')
        # check if exist record
        record_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        record_d = record_dt.date()
        exist_record = indicator_obj.indicator_records.filter(
                date=record_d, user=request.user)
        if exist_record:
            data = {'failed': True, 'error_code': 20,
                    'error_string': 'record_exist'}
            return HttpResponse(json.dumps(data),
                    mimetype='application/json')
        # val_min
        if val_min_str:
            val_min = float(val_min_str)
        else:
            val_min = None
        # val_max
        if val_max_str:
            val_max = float(val_max_str)
        else:
            val_max = None
        # create record (NOTE: use "standard" unit)
        new_record = im.IndicatorRecord(
            indicator=indicator_obj,
            user=request.user,
            date=record_d,
            unit=indicator_obj.get_unit(type="standard")[0],
            value=value,
            val_min=val_min,
            val_max=val_max,
            notes=u""
        )
        if new_record.is_valid():
            # True -> Valid; save
            new_record.save()
            # generate result {{{
            dataType = indicator_obj.dataType
            if dataType == im.Indicator.INTEGER_TYPE:
                # TODO
                record_value_html = format_data(indicator_obj,
                        value=new_record.value, type="html")
                record_value_text = format_data(indicator_obj,
                        value=new_record.value, type="text")
            elif dataType == im.Indicator.FLOAT_TYPE:
                record_value_html = format_data(indicator_obj,
                        value=new_record.value, type="html")
                record_value_text = format_data(indicator_obj,
                        value=new_record.value, type="text")
            elif dataType == im.Indicator.RANGE_TYPE:
                record_value_html = format_data(indicator_obj,
                        val_min=new_record.val_min,
                        val_max=new_record.val_max, type="html")
                record_value_text = format_data(indicator_obj,
                        val_min=new_record.val_min,
                        val_max=new_record.val_max, type="text")
            elif dataType == im.Indicator.FLOAT_RANGE_TYPE:
                # TODO
                record_value_html = u"TODO"
                record_value_text = u"TODO"
            elif dataType == im.Indicator.PM_TYPE:
                record_value_html = format_data(indicator_obj,
                        value=new_record.value, type="html")
                record_value_text = format_data(indicator_obj,
                        value=new_record.value, type="text")
            else:
                record_value_html = None
                record_value_text = None
            data = {
                'failed': False,
                'record_id': new_record.id,
                'date': new_record.date.isoformat(),
                'value': new_record.value,
                'val_min': new_record.val_min,
                'val_max': new_record.val_max,
                'value_html': record_value_html,
                'value_text': record_value_text
            }
            # }}}
        else:
            # invalid
            data = {'failed': True, 'error_code': 30,
                    'error_string': 'record_invalid' }

    print "data: ", data
    return HttpResponse(json.dumps(data), mimetype='application/json')
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


# ajax_get_card_data_chart {{{
@login_required
def ajax_get_card_data_chart(request):
    """
    'indicator/static/javascripts/card_chart.js'
    get card data
    for the 'chart' within the card
    format: [[UTC_ms1, v1], [UTC_ms2, v2], [UTC_ms3, v3], ...]

    NOTE: UTC_ms: is the 'ms' from '1970-01-01T00:00.00Z'
    GET parameters:
    begin, end, format: 'YYYY-MM-DD', '%Y-%m-%d'
    '%Y-%m-%dT%H:%M:%S.%fZ'
    """
    # default parameters
    data = {'failed': True}
    begin = None
    end = None
    num = None
    #
    #if True:
    if request.is_ajax():
        # check card_id -> indicator_id
        if request.GET.get('card_id') is not None:
            card_id = request.GET.get('card_id')
            try:
                indicator_id = int(card_id)
                ind_obj = im.Indicator.objects.get(id=indicator_id)
            except ValueError:
                print u'Error: Given card_id="%s" cannot convert to integer' % card_id
                raise Http404
            except im.Indicator.DoesNotExist:
                print u'Error: Indicator id="%s" NOT exist' % indicator_id
                raise Http404
        else:
            print u'Error: No card_id provided'
            raise Http404
        # check 'type': num/date
        if request.GET.get('type') == 'num':
            # type: 'num'
            type = request.GET.get('type')
        elif request.GET.get('type') == 'date':
            # type: 'date'
            type = request.GET.get('type')
        else:
            print u'Error: unknown type="%s"' % request.GET.get('type')
            raise Http404
        # check 'num'
        if request.GET.get('num'):
            num = request.GET.get('num')
        else:
            # 'num' not given, or empty string
            num = None
        # begin datetime
        if request.GET.get('begin'):
            begin = request.GET.get('begin')
        else:
            begin = None
        # end datetime
        if request.GET.get('end'):
            end = request.GET.get('end')
        else:
            end = None

        # type 'num'
        if type == 'num':
            # check 'num'
            if not num:
                raise ValueError(u"Error: num NOT specified")
                raise Http404
            try:
                num = int(num)
            except ValueError:
                raise ValueError(u"Error: num='%s' NOT valid" % num)
                raise Http404
            # check 'end'
            if end:
                try:
                    end_datetime = datetime.datetime.strptime(end,
                            '%Y-%m-%d')
                    end_date = end_datetime.date()
                except ValueError:
                    raise ValueError(u'Error: Given end="%s" invalid' % end)
                    raise Http404
            else:
                end_date = None
            # get records
            records_data = get_num_record_std(user_id=request.user.id,
                    indicator_id=indicator_id,
                    number=num, end=end_date)
        else:
            # type 'date'
            # check 'end'
            if begin:
                try:
                    begin_datetime = datetime.datetime.strptime(begin,
                            '%Y-%m-%d')
                    begin_date = begin_datetime.date()
                except ValueError:
                    raise ValueError(u'Error: Given begin="%s" invalid' % begin)
                    raise Http404
            else:
                begin_date = None
            # check 'end'
            if end:
                try:
                    end_datetime = datetime.datetime.strptime(end,
                            '%Y-%m-%d')
                    end_date = end_datetime.date()
                except ValueError:
                    raise ValueError(u'Error: Given end="%s" invalid' % end)
                    raise Http404
            else:
                end_date = None
            # get records
            records_data = get_record_std(user_id=request.user.id,
                    indicator_id=indicator_id,
                    begin=begin_date, end=end_date)

        #
        if not records_data['failed']:
            # success
            data = records_data.copy()
            data['data'] = []
            dataType = ind_obj.dataType
            unix_begin = datetime.datetime(1970, 1, 1, 0, 0)
            for r in records_data['data']:
                dt = datetime.datetime.strptime(r['date'], '%Y-%m-%d')
                time_ms = (dt-unix_begin).total_seconds() * 1000.0
                if dataType == im.Indicator.INTEGER_TYPE:
                    # TODO
                    pass
                elif dataType == im.Indicator.FLOAT_TYPE:
                    value = r['value']
                    data['data'].append([time_ms, value])
                elif dataType == im.Indicator.RANGE_TYPE:
                    val_min = r['val_min']
                    val_max = r['val_max']
                    data['data'].append([time_ms, val_min, val_max])
                elif dataType == im.Indicator.FLOAT_RANGE_TYPE:
                    # TODO
                    pass
                elif dataType == im.Indicator.PM_TYPE:
                    # TODO
                    pass
                else:
                    print u'Error: unknow dataType'
                    data = {'failed': True}
                    return HttpResponse(json.dumps(data),
                            mimetype='application/json')
    #
    return HttpResponse(json.dumps(data), mimetype='application/json')
# }}}


# ajax_get_card_data_table {{{
@login_required
def ajax_get_card_data_table(request):
    """
    'indicator/static/javascripts/card_chart.js'
    get card data
    for used in 'detail card table'
    """
    # default parameters
    data = {'failed': True}
    begin = None
    end = None
    num = None
    #
    #if True:
    if request.is_ajax():
        # get parameters {{{
        # check card_id -> indicator_id
        if request.GET.get('card_id') is not None:
            card_id = request.GET.get('card_id')
            try:
                indicator_id = int(card_id)
                ind_obj = im.Indicator.objects.get(id=indicator_id)
            except ValueError:
                print u'Error: Given card_id="%s" cannot convert to integer' % card_id
                raise Http404
            except im.Indicator.DoesNotExist:
                print u'Error: Indicator id="%s" NOT exist' % indicator_id
                raise Http404
        else:
            print u'Error: No card_id provided'
            raise Http404
        # check 'type': num/date
        if request.GET.get('type') == 'num':
            # type: 'num'
            type = request.GET.get('type')
        elif request.GET.get('type') == 'date':
            # type: 'date'
            type = request.GET.get('type')
        else:
            print u'Error: unknown type="%s"' % request.GET.get('type')
            raise Http404
        # check 'num'
        if request.GET.get('num'):
            num = request.GET.get('num')
        else:
            # 'num' not given, or empty string
            num = None
        # begin datetime
        if request.GET.get('begin'):
            begin = request.GET.get('begin')
        else:
            begin = None
        # end datetime
        if request.GET.get('end'):
            end = request.GET.get('end')
        else:
            end = None
        # }}}

        # get record data {{{
        # type 'num'
        if type == 'num':
            # check 'num'
            if not num:
                raise ValueError(u"Error: num NOT specified")
                raise Http404
            try:
                num = int(num)
            except ValueError:
                raise ValueError(u"Error: num='%s' NOT valid" % num)
                raise Http404
            # check 'end'
            if end:
                try:
                    end_datetime = datetime.datetime.strptime(end,
                            '%Y-%m-%d')
                    end_date = end_datetime.date()
                except ValueError:
                    raise ValueError(u'Error: Given end="%s" invalid' % end)
                    raise Http404
            else:
                end_date = None
            # get records
            records_data = get_num_record_std(user_id=request.user.id,
                    indicator_id=indicator_id,
                    number=num, end=end_date)
        else:
            # type 'date'
            # check 'end'
            if begin:
                try:
                    begin_datetime = datetime.datetime.strptime(begin,
                            '%Y-%m-%d')
                    begin_date = begin_datetime.date()
                except ValueError:
                    raise ValueError(u'Error: Given begin="%s" invalid' % begin)
                    raise Http404
            else:
                begin_date = None
            # check 'end'
            if end:
                try:
                    end_datetime = datetime.datetime.strptime(end,
                            '%Y-%m-%d')
                    end_date = end_datetime.date()
                except ValueError:
                    raise ValueError(u'Error: Given end="%s" invalid' % end)
                    raise Http404
            else:
                end_date = None
            # get records
            records_data = get_record_std(user_id=request.user.id,
                    indicator_id=indicator_id,
                    begin=begin_date, end=end_date)
        # }}}

        #
        if not records_data['failed']:
            # success
            data = records_data.copy()
            data['data'] = []   # clear original data
            r_data = []         # store processed 'r' dicts
            dataType = ind_obj.dataType
            for r in records_data['data']:
                r_id = r['id']
                r_obj = im.IndicatorRecord.objects.get(id=r_id)
                r['is_normal'] = r_obj.is_normal() # True|False|None
                r['std_unit_name'] = r['unit'].get('name') # maybe None
                r['std_unit_symbol'] = r['unit'].get('symbol')
                # check dataType
                if dataType == im.Indicator.INTEGER_TYPE:
                    # TODO
                    r['value_html'] = ""
                    pass
                elif dataType == im.Indicator.FLOAT_TYPE:
                    value = r['value']
                    r['value_html'] = format_data(ind_obj,
                            value=value, type="html")
                elif dataType == im.Indicator.RANGE_TYPE:
                    val_min = r['val_min']
                    val_max = r['val_max']
                    r['value_html'] = format_data(ind_obj,
                            val_min=val_min, val_max=val_max,
                            type="html")
                elif dataType == im.Indicator.FLOAT_RANGE_TYPE:
                    # TODO
                    r['value_html'] = ""
                    pass
                elif dataType == im.Indicator.PM_TYPE:
                    # TODO
                    r['value_html'] = ""
                    pass
                else:
                    print u'Error: unknow dataType'
                    data = {'failed': True}
                    return HttpResponse(json.dumps(data),
                            mimetype='application/json')
                # 'r' dict updated, append to 'r_data'
                r_data.append(r)
            # endfor
            # sort 'r_data' by '-date', newest comes first
            r_data.sort(key = lambda item: item['date'])
            r_data.reverse()
            # update 'data'
            data['data'] = r_data
    #
    return HttpResponse(json.dumps(data), mimetype='application/json')
# }}}


# ajax_search_indicators {{{
@login_required
def ajax_search_indicators(request):
    """
    search indicators
    search keyword passed by 'GET' parameters
    """
    data = {'failed': True, 'error_code': 1, 'error_string': 'unknow'}
    if True:
    #if request.is_ajax():
        if 'kw' in request.GET:
            # kw: search keyword to find indicator
            search_kw = request.GET.get('kw')
            # check search keyword
            if not search_kw.strip():
                data = {'failed': True, 'error_code': 10,
                        'error_string': 'blank_keyword'}
            else:
                # TODO: howto order_by() by 'pinyin'
                sqs = SearchQuerySet().models(im.Indicator).\
                        filter(content=search_kw)
                if sqs:
                    # search result not empty
                    inds_unsort = [ind.dump()
                            for ind in objects_of_sqs(sqs)]
                    indicators = sorted(inds_unsort,
                            key = lambda item: item['pinyin'])
                    # process results
                    data = {'failed': False, 'indicators': indicators}
                else:
                    # search result empty
                    data = {'failed': True, 'error_code': 20,
                            'error_string': 'result_empty',
                            'empty': True}

    return HttpResponse(json.dumps(data), mimetype='application/json')
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


# ajax_modify_record {{{
@login_required
def ajax_modify_record(request):
    """
    modify the existing record using the POSTed data
    and add a 'RecordHistory' for the record

    error_code & error_string:
      1: unknown
     10: record_id
     20: recordhistory
     30: record_invalid
    """
    data = {'failed': True, 'error_code': 1, 'error_string': 'unknown'}
    #if request.method == 'POST':
    if request.is_ajax() and request.method == 'POST':
        #print request.POST.dict()
        record_id = request.POST.get('record_id')
        date_str = request.POST.get('date')
        value = request.POST.get('value')
        val_min_str = request.POST.get('val_min')
        val_max_str = request.POST.get('val_max')
        reason = request.POST.get('reason')
        created_at_str = request.POST.get('created_at')
        # get record object
        try:
            record_id = int(record_id)
            record_obj = get_object_or_404(im.IndicatorRecord,
                    id=record_id)
        except ValueError:
            data = {
                'failed': True,
                'error_code': 10,
                'error_string': 'record_id'
            }
            return HttpResponse(json.dumps(data),
                    mimetype='application/json')
        # add RecordHistory
        created_at = datetime.datetime.strptime(created_at_str,
                '%Y-%m-%dT%H:%M:%S.%fZ')
        rh_flag = add_recordhistory(user_id=request.user.id,
                record_id=record_id, reason=reason,
                created_at=created_at)
        if rh_flag == False:
            data = {
                'failed': True,
                'error_code': 20,
                'error_string': 'recordhistory'
            }
            return HttpResponse(json.dumps(data),
                    mimetype='application/json')
        # record
        updated_at = created_at.replace(tzinfo=utc)
        date_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        date_d = date_dt.date()
        # val_min
        if val_min_str:
            val_min = float(val_min_str)
        else:
            val_min = None
        # val_max
        if val_max_str:
            val_max = float(val_max_str)
        else:
            val_max = None
        # update record
        record_obj.updated_at = updated_at
        record_obj.date = date_d
        record_obj.value = value
        record_obj.val_min = val_min
        record_obj.val_max = val_max
        r_flag = record_obj.is_valid()
        if r_flag:
            # save
            record_obj.save()
            data = { 'failed': False }
        else:
            data = { 'failed': True, 'error_code': 30,
                     'error_string': 'record_invalid' }

    return HttpResponse(json.dumps(data), mimetype='application/json')
# }}}


###########################################################

### test_view ### {{{
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

    boolvar = False

    data = {
        'all_letters': all_letters,
        'all_indicators': all_indicators,
        'followed_indicators': followed_indicators,
        'list': list,
        'boolvar': boolvar,
    }
    return render(request, template, data)
# test }}}

