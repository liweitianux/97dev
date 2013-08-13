# -*- coding: utf-8 -*-

"""
utils for apps/indicator
"""

from django.contrib.auth.models import User

from indicator import models as im
from sciblog import models as sciblogm

import datetime


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
    iqueryset = im.Indicator.objects.exclude(user_indicators=ui)
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


# calc_indicator_weight {{{
def calc_indicator_weight(user_id, indicator_id):
    """
    calculate the weight of given indicator
    used by 'recommend_indicator'
    """
    ### XXX: weight_type: how to store the weights into database ###
    weight_annotation = 4.0
    weight_blog_catched = 3.0
    weight_blog_collected = 2.0
    weight_other = 1.0
    ################################################################
    # weight = weight_type * relatedindicator.weight
    user = User.objects.get(id=user_id)
    ri_qs = im.RelatedIndicator.objects.filter(indicator__id=indicator_id)
    if not ri_qs:
        # queryset empty
        w = 0.0
        return w
    # queryset not empty
    annotation_ri_qs = ri_qs.filter(annotation__collected_by=user)
    blogcatch_ri_qs = ri_qs.filter(blog__catched_by=user)
    blogcollect_ri_qs = ri_qs.filter(blog__collected_by=user)
    weights = []
    if annotation_ri_qs:
        # related to annotations collected by user
        for ri in annotation_ri_qs:
            w = weight_annotation * ri.weight
            weights.append(w)
    elif blogcatch_ri_qs:
        # related to blogs catched by user
        for ri in blogcatch_ri_qs:
            w = weight_blog_catched * ri.weight
            weights.append(w)
    elif blogcollect_ri_qs:
        # related to blogs catched by user
        for ri in blogcollect_ri_qs:
            w = weight_blog_collected * ri.weight
            weights.append(w)
    else:
        # other type, use 'ri_qs' here
        for ri in ri_qs:
            w = weight_other * ri.weight
            weights.append(w)
    # return final result
    return max(weights)
# }}}


# recommend_indicator {{{
def recommend_indicator(user_id, number):
    """
    recommend unfollowed indicator for user,
    based on his/her readings and collections.

    return a list with the id's of recommended indicators

    TODO:
    performance test
    """
    user_id = int(user_id)
    number = int(number)
    # get unfollowed indicators
    u = User.objects.get(id=user_id)
    ui, created = im.UserIndicator.objects.get_or_create(user=u)
    uf_ind_qs = im.Indicator.objects.exclude(user_indicators=ui)
    # calc weight for each unfollowed indicator
    weights = []
    for ind in uf_ind_qs:
        w = calc_indicator_weight(user_id, ind.id)
        weights.append({'id': ind.id, 'weight': w})
    # sort 'weights' dict list by key 'weight'
    weights_sorted = sorted(weights, key=lambda item: item['weight'])
    weights_sorted.reverse()
    # return results with largest weights
    return weights_sorted[:number]
# }}}


