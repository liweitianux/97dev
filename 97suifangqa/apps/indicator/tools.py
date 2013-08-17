# -*- coding: utf-8 -*-

"""
utils for apps/indicator
"""

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from indicator import models as im
from sciblog import models as sciblogm

import re
import datetime


# follow_indicator {{{
def follow_indicator(user_id, indicator_id):
    """
    用户关注指标
    """
    try:
        user = get_object_or_404(User, id=user_id)
        indicator = im.Indicator.objects.get(id=indicator_id)
        ui, created = im.UserIndicator.objects.get_or_create(user=user)
        ui.followedIndicators.add(indicator)
        # to remove the indicator from 'followedHistories' if exists
        if indicator in ui.followedHistories.all():
            ui.followedHistories.remove(indicator)
        return True
    except:
        return False
# }}}


# unfollow_indicator {{{
def unfollow_indicator(user_id, indicator_id):
    """
    用户取消关注指标
    """
    try:
        user = get_object_or_404(User, id=user_id)
        indicator = im.Indicator.objects.get(id=indicator_id)
        ui, created = im.UserIndicator.objects.get_or_create(user=user)
        ui.followedIndicators.remove(indicator)
        # add indicator to 'followedHistories'
        ui.followedHistories.add(indicator)
        return True
    except:
        return False
# }}}


# get_indicator {{{
def get_indicator(category_id="all", startswith="all"):
    """
    根据指定的 category_id 和 startswith 获取 indicator
    返回一个 dict
    Dict format:
    dict = {
        'a': [ {'pinyin': 'aa', ...}, {'pinyin': 'ab', ...}, ... ],
        'b': [ {'pinyin': 'ba', ...}, {'pinyin': 'bb', ...}, ... ],
        ...
    }
    """

    _idict = {}
    if category_id == 'all':
        iqueryset = im.Indicator.objects.all()
    else:
        try:
            cid = int(category_id)
            cate = im.IndicatorCategory.objects.get(id=cid)
            iqueryset = cate.indicators.all()
        except ValueError:
            raise ValueError(u'category_id 不是整数型')
            return _idict
        except im.IndicatorCategory.DoesNotExist:
            raise ValueError(u'id=%s 的 IndicatorCategory 不存在'
                    % cid)
            return _idict

    if startswith == 'all':
        starts = map(chr, range(ord('a'), ord('z')+1))
    else:
        starts = []
        _str = startswith.lower()
        for i in _str:
            if i >= 'a' and i <= 'z':
                starts.append(i)

    for l in starts:
        iq = iqueryset.filter(pinyin__istartswith=l).order_by('pinyin')
        _idict[l] = [ i.dump() for i in iq ]
    return _idict
# }}}


# get_followed_indicator {{{
def get_followed_indicator(user_id, category_id="all", startswith="all"):
    """
    获取已关注的指标
    返回 dict, 格式与 get_indicator() 一致
    """

    u = User.objects.get(id=user_id)
    ui, created = im.UserIndicator.objects.get_or_create(user=u)
    _idict = {}
    iqueryset = ui.followedIndicators.all()
    if not category_id == 'all':
        try:
            cid = int(category_id)
            iqueryset = iqueryset.filter(categories__id=cid)
        except ValueError:
            raise ValueError(u'category_id 不是整数型')
            return _idict

    if startswith == 'all':
        starts = map(chr, range(ord('a'), ord('z')+1))
    else:
        starts = []
        _str = startswith.lower()
        for i in _str:
            if i >= 'a' and i <= 'z':
                starts.append(i)

    for l in starts:
        iq = iqueryset.filter(pinyin__istartswith=l).order_by('pinyin')
        _idict[l] = [ i.dump() for i in iq ]
    return _idict
# }}}


# get_unfollowed_indicator {{{
def get_unfollowed_indicator(user_id, category_id="all", startswith="all"):
    """
    获取未关注的指标
    返回 dict, 格式与 get_indicator() 一致
    """

    u = User.objects.get(id=user_id)
    ui, created = im.UserIndicator.objects.get_or_create(user=u)
    _idict = {}
    # XXX: if 'exclude(followed_indicators=ui)' OK??
    iqueryset = im.Indicator.objects.exclude(followed_indicators=ui)
    if not category_id == 'all':
        try:
            cid = int(category_id)
            iqueryset = iqueryset.filter(categories__id=cid)
        except ValueError:
            raise ValueError(u'category_id 不是整数型')
            return _idict

    if startswith == 'all':
        starts = map(chr, range(ord('a'), ord('z')+1))
    else:
        starts = []
        _str = startswith.lower()
        for i in _str:
            if i >= 'a' and i <= 'z':
                starts.append(i)

    for l in starts:
        iq = iqueryset.filter(pinyin__istartswith=l).order_by('pinyin')
        _idict[l] = [ i.dump() for i in iq ]
    return _idict
# }}}


# get_record {{{
def get_record(user_id, indicator_id, begin="", end="", std=False):
    """
    get_record(user_id, indicator_id, begin="", end="", std=False)

    return a dict with 'date' as key, and 'get_data()' as value.
    args 'begin' and 'end' to specify the date range.
    arg 'std=True' to get data in standard unit
    if 'begin=""', then the earliest date is given;
    if 'end=""', then the latest date is given.

    return dict format:
    rdata = {
        'date1': [d1r1.get_data(), d1r2.get_data(), ...],
        'date2': [d2r1.get_data(), d2r2.get_data(), ...],
        ...
    }
    """
    uid = int(user_id)
    indid = int(indicator_id)
    all_records = im.IndicatorRecord.objects.\
            filter(user__id=uid, indicator__id=indid).\
            order_by('date', 'created_at')
    # check if 'all_records' empty
    if not all_records:
        return {}
    # set 'begin' and 'end'
    if begin == '':
        begin = all_records[0].date
    if end == '':
        end = all_records.reverse()[0].date
    # check the validity of given 'begin' and 'end'
    if (isinstance(begin, datetime.date) and
            isinstance(end, datetime.date)):
        records = all_records.filter(date__range=(begin, end))
        _rdata = {}
        for r in records:
            _d = r.date.isoformat()
            # get data
            if std:
                _data = r.get_data_std()
            else:
                _data = r.get_data()
            #
            if _rdata.has_key(_d):
                # the date key already exist
                _rdata[_d] += [_data]
            else:
                # the date key not exist
                _rdata[_d] = [_data]
        # return
        return _rdata
    else:
        raise ValueError(u"begin='%s' or end='%s' 不是合法的日期" %
                (begin, end))
        return {}
# }}}


# get_record_std {{{
def get_record_std(**kwargs):
    return get_record(std=True, **kwargs)
# }}}


# types of recommended indicators, and weights {{{
RI_TYPES = {
    'ANNOTATION_COLLECTED': u'ANN_CL',
    'BLOG_CATCHED': u'BLG_CT',
    'BLOG_COLLECTED': u'BLG_CL',
    'OTHER': u'OTHER',
    'ERROR': u'ERROR',      # no 'RelatedIndicator' data
}
RI_WEIGHTS = {
    RI_TYPES['ANNOTATION_COLLECTED']: 4.0,
    RI_TYPES['BLOG_CATCHED']: 3.0,
    RI_TYPES['BLOG_COLLECTED']: 2.0,
    RI_TYPES['OTHER']: 1.0,
    RI_TYPES['ERROR']: 0.0,
}
# }}}


# calc_indicator_weight {{{
def calc_indicator_weight(user_id, indicator_id):
    """
    calculate the weight of given indicator
    used by 'recommend_indicator'

    return format:
    {'weight': w, 'type': t}
    """
    # weight = weight_type * relatedindicator.weight
    user = User.objects.get(id=user_id)
    ri_qs = im.RelatedIndicator.objects.filter(indicator__id=indicator_id)
    if not ri_qs:
        # queryset empty: no 'RelatedIndicator' for this indicator
        type = RI_TYPES['ERROR']
        w = 0.0
        return {'weight': w, 'type': type}
    # queryset not empty
    annotation_ri_qs = ri_qs.filter(annotation__collected_by=user)
    blogcatch_ri_qs = ri_qs.filter(blog__catched_by=user)
    blogcollect_ri_qs = ri_qs.filter(blog__collected_by=user)
    weights = []
    if annotation_ri_qs:
        # related to annotations collected by user
        type = RI_TYPES['ANNOTATION_COLLECTED']
        for ri in annotation_ri_qs:
            w = RI_WEIGHTS[type] * ri.weight
            weights.append({'weight': w, 'type': type})
    elif blogcatch_ri_qs:
        # related to blogs catched by user
        type = RI_TYPES['BLOG_CATCHED']
        for ri in blogcatch_ri_qs:
            w = RI_WEIGHTS[type] * ri.weight
            weights.append({'weight': w, 'type': type})
    elif blogcollect_ri_qs:
        # related to blogs collected by user
        type = RI_TYPES['BLOG_COLLECTED']
        for ri in blogcollect_ri_qs:
            w = RI_WEIGHTS[type] * ri.weight
            weights.append({'weight': w, 'type': type})
    else:
        # other type, use 'ri_qs' here
        type = RI_TYPES['OTHER']
        for ri in ri_qs:
            w = RI_WEIGHTS[type] * ri.weight
            weights.append({'weight': w, 'type': type})
    # sort results
    weights_sorted = sorted(weights, key = lambda item: item['weight'])
    # return final result
    return weights_sorted[-1]
# }}}


# recommend_indicator {{{
def recommend_indicator(user_id, number):
    """
    recommend unfollowed indicator for user,
    based on his/her readings and collections.

    return a list of recommended indicators in format:
    [ {'id': id, 'weight': w, 'type': t}, ... ]
    """
    user_id = int(user_id)
    number = int(number)
    # get unfollowed indicators
    u = User.objects.get(id=user_id)
    ui, created = im.UserIndicator.objects.get_or_create(user=u)
    # XXX: if 'exclude(followed_indicators=ui)' OK??
    uf_ind_qs = im.Indicator.objects.exclude(followed_indicators=ui)
    # calc weight for each unfollowed indicator
    weights = []
    for ind in uf_ind_qs:
        wdict = calc_indicator_weight(user_id, ind.id)
        weights.append({
            'id': ind.id,
            'weight': wdict.get('weight'),
            'type': wdict.get('type'),
        })
    # sort 'weights' dict list by key 'weight'
    weights_sorted = sorted(weights, key=lambda item: item['weight'])
    weights_sorted.reverse()
    # return results with largest weights
    return weights_sorted[:number]
# }}}


# format_data {{{
def format_data(indicator_obj, value=None, val_max=None, val_min=None):
    """
    format given data according to the dataType of given Indicator,
    make it proper for django templates
    e.g.:
    if number very big, then display in 'exponent notation'

    used in '.views.indicator_status()'
    """
    # threshold to show a float number in scientific notation
    float_threshold = 9999.9
    # float display format: fixed point, exponent notation
    fix_fmt = '{:,.1f}'    # comma as a thousands separator
    exp_fmt = '{:.2e}'
    # regex to process exponent notation
    rep = re.compile(r'^(?P<sign>[-+]?)(?P<num>\d\.\d+)[eE]\+?(?P<expminus>-?)0*(?P<exp>[1-9]+)$')
    # range symbol (range: low $symbol$ high)
    range_sym = '&sim;'
    # default return value
    value_str = u''

    # check given 'indicator_obj'
    ind = indicator_obj
    if not isinstance(ind, im.Indicator):
        print u'Error: given indicator_obj NOT a instance of Indicator'
        raise ValueError(u'Given indicator_obj NOT a instance of Indicator')
    # get dataType
    dataType = ind.dataType

    if value is not None:
        # a) record float data; b) record integer/pm data;
        # c) confine integer/pm data.
        if dataType == ind.INTEGER_TYPE:
            # TODO: process 'integer type' data
            value_str = u'INTEGER: %s' % value
        elif dataType == ind.PM_TYPE:
            if value == u'+':
                value_str = u'阳性(+)'
            else:
                value_str = u'阳性(-)'
        elif dataType in [ind.FLOAT_TYPE, ind.FLOAT_RANGE_TYPE]:
            # process float number
            value = float(value)
            if value <= float_threshold:
                value_str = fix_fmt.format(value)
            else:
                value_expstr = exp_fmt.format(value)
                # convert to html exponent format
                m = rep.match(value_expstr)
                value_str = "%s%s&times;10<sup>%s%s</sup>" % (
                        m.group('sign'), m.group('num'),
                        m.group('expminus'), m.group('exp'))
        else:
            # unknown XXX
            pass
    elif (val_max is not None) and (val_min is not None):
        # a) record range data; b) confine range.
        # val_max
        if val_max <= float_threshold:
            val_max_str = fix_fmt.format(val_max)
        else:
            val_max_expstr = exp_fmt.format(val_max)
            # convert to html exponent format
            m = rep.match(val_max_expstr)
            val_max_str = "%s%s&times;10<sup>%s%s</sup>" % (
                    m.group('sign'), m.group('num'),
                    m.group('expminus'), m.group('exp'))
        # val_min
        if val_min <= float_threshold:
            val_min_str = fix_fmt.format(val_min)
        else:
            val_min_expstr = exp_fmt.format(val_min)
            # convert to html exponent format
            m = rep.match(val_min_expstr)
            val_min_str = "%s%s&times;10<sup>%s%s</sup>" % (
                    m.group('sign'), m.group('num'),
                    m.group('expminus'), m.group('exp'))
        # value_str
        value_str = u'%s %s %s' % (val_min_str, range_sym, val_max_str)
    else:
        # other type??
        pass

    return value_str
# }}}

