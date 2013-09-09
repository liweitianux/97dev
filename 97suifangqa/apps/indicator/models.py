# -*- coding: utf-8 -*-
#
# Weitian Li <liweitianux@foxmail.com>
# updated: 2013/08/12
#

"""
apps/indicator models
"""

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# '@permalink' is no longer recommended
from django.core.urlresolvers import reverse

import re
import datetime

import sympy
from sympy.core.sympify import SympifyError

from utils.xpinyin import Pinyin


class IndicatorCategory(models.Model):                      # {{{
    """
    对 Indicator 进行分类，用于前端按分类显示和选择指标。
    """
    name = models.CharField(u"指标类别名称", max_length=100)
    pinyin = models.CharField(u"拼音", max_length=200,
            editable=False, blank=True)
    englishName = models.CharField(u"Indicator Category Name",
            max_length=200, blank=True)
    description = models.TextField(u"指标类别描述", blank=True)
    # 记录添加的用户，用户只能修改自己添加的对象
    addByUser = models.ForeignKey(User, verbose_name=u"添加的用户",
            related_name="indicator_categories")

    class Meta:
        verbose_name_plural = u"指标类别"
        ordering = ['pinyin', 'id']

    def __unicode__(self):
        return u"< IndicatorCategory: #%s, %s addBy %s >"\
                % (self.id, self.name, self.addByUser.username)

    def show(self):
        """
        used in 'search/search.html'
        to show search result
        """
        return self.__unicode__()

    def get_absolute_url(self):
        # need define url with name='show_category', 'pk' as parameter
        return reverse('show_category',
                kwargs={'pk': self.id})

    # auto generate `pinyin'
    def save(self, **kwargs):
        p = Pinyin()
        self.pinyin = p.get_pinyin(self.name)
        super(IndicatorCategory, self).save(**kwargs)

    def dump(self, **kwargs):
        dump_data = {
            'id': self.id,
            'name': self.name,
            'pinyin': self.pinyin,
            'englishName': self.englishName,
            'description': self.description,
            'addByUser_id': self.addByUser.id,
        }
        return dump_data
# }}}


class Indicator(models.Model):                              # {{{
    """
    指标模型
    """
    name = models.CharField(u"指标名称", max_length=100)
    pinyin = models.CharField(u"拼音", max_length=200,
            editable=False, blank=True)
    englishName = models.CharField(u"Indicator Name",
            max_length=200, blank=True)
    description = models.TextField(u"指标描述", blank=True)
    # Indicator 接受数据类型/格式等说明/示例
    helpText = models.CharField(u"帮助", max_length=300, blank=True)
    # 记录添加指标的用户，用户只能修改自己添加的指标
    addByUser = models.ForeignKey(User, verbose_name=u"添加的用户",
            related_name="indicators")
    # Category
    categories = models.ManyToManyField(IndicatorCategory,
            verbose_name=u"所属类别", related_name="indicators")
    # DATA_TYPES for indicator
    INTEGER_TYPE = u'IN'        # 整数型
    FLOAT_TYPE = u'FL'          # 浮点型
    RANGE_TYPE = u'RG'          # 范围型(eg. 250-500)
    FLOAT_RANGE_TYPE = u'FR'    # 浮点型/范围型，接受定值或范围
    PM_TYPE = u'PM'             # +/- 型
    RADIO_TYPE = u'RD'          # 单选型
    CHECKBOX_TYPE = u'CB'       # 多选多
    DATA_TYPES = (
        (INTEGER_TYPE, u"整数型"),
        (FLOAT_TYPE, u"浮点定值型"),
        (RANGE_TYPE, u"浮点范围型"),
        (FLOAT_RANGE_TYPE, u"定值或范围型"),
        (PM_TYPE, u"阴阳型(+/-)"),
        #(RADIO_TYPE, u"单选型"),
        #(CHECKBOX_TYPE, u"多选型"),
    )
    dataType = models.CharField(u"数据类型", max_length=2,
            choices=DATA_TYPES)

    class Meta:
        verbose_name_plural = u"医学指标"
        ordering = ['pinyin', 'id']

    def __unicode__(self):
        return u"< Indicator: #%s, %s, dataType %s addBy %s >"\
                % (self.id, self.name, self.dataType,
                self.addByUser.username)

    def show(self):
        """
        used in 'search/search.html'
        to show search result
        """
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('show_indicator',
                kwargs={'pk': self.id})

    # auto generate `pinyin'
    def save(self, **kwargs):
        p = Pinyin()
        self.pinyin = p.get_pinyin(self.name)
        super(Indicator, self).save(**kwargs)

    def check_unit(self, **kwargs):
        """
        Check if the validity of the units specified for the indicator.
        A indicator must have one 'standard unit'.
        if indicator.dataType in [INTEGER_TYPE, PM_TYPE],
        then units are not needed.
        """
        if self.dataType in [self.FLOAT_TYPE, self.RANGE_TYPE,
                self.FLOAT_RANGE_TYPE]:
            std_unit = self.units.filter(standard=True)
            if std_unit:
                return True
            else:
                print u"Indicator id=%s 未指定标准单位" % self.id
                return False
        else:
            print u"dataType=%s 不需要单位" % self.dataType
            return True

    def _get_unit(self, type="standard"):
        if type == "standard":
            _units = self.units.filter(standard=True)
        elif type == "other":
            _units = self.units.filter(standard=False)
        else:
            _units = []
        return list(_units)

    def get_unit(self, type="standard"):
        """
        return a 'list' which contains the 'Unit's
        related to the indicator
            get_unit(type):
                type = standard(default), other, all
        this return the 'standard unit' by default
        if 'type="all"', the 'standard unit' comes first
        """
        if type == "all":
            # get all units
            # standard unit first
            _units = self._get_unit(type="standard")\
                    + self._get_unit(type="other")
            return _units
        else:
            return self._get_unit(type)

    def check_confine(self):
        """
        check the existence of the related InnateConfine
        """
        try:
            c = self.innate_confine
            return True
        except InnateConfine.DoesNotExist:
            print u'Indicator id=%s 未指定 InnateConfine' % self.id
            raise ValueError(u'Indicator id=%s 未指定 InnateConfine'
                    % self.id)
            return False

    def get_confine(self):
        """
        dump the confine data from the related InnateConfine
        """
        try:
            c = self.innate_confine
            return c.dump()
        except InnateConfine.DoesNotExist:
            print u'Indicator id=%s 未指定 InnateConfine' % self.id
            return {}

    def is_ready(self):
        """
        check the status of this indicator,
        if 'Unit's and 'InnateConfine' are correctly specified,
        then the Indicator is ready to use. returned 'True'
        """
        return (self.check_unit() and self.check_confine())

    def dump(self, **kwargs):
        dump_data = {
            'id': self.id,
            'name': self.name,
            'pinyin': self.pinyin,
            'englishName': self.englishName,
            'description': self.description,
            'helpText': self.helpText,
            'addByUser_id': self.addByUser.id,
            'dataType': self.dataType,
            'categories_id': [c.id
                for c in self.categories.all()],
            'categories_name': [c.name
                for c in self.categories.all()],
            'units_id': [u.id
                for u in self.get_unit(type="all")]
        }
        return dump_data
# }}}


class UserIndicator(models.Model):                          # {{{
    """
    记录某用户关注了哪些指标
    """
    user = models.OneToOneField(User, verbose_name=u"用户",
            related_name="user_indicator")
    followedIndicators = models.ManyToManyField(Indicator,
            verbose_name=u"关注的指标",
            related_name="followed_indicators",
            null=True, blank=True)
    followedHistories = models.ManyToManyField(Indicator,
            verbose_name=u"历史关注指标",
            related_name="followed_histories",
            null=True, blank=True)
    # TODO
    # last_recommend_time

    class Meta:
        verbose_name_plural = u"用户指标信息"

    def __unicode__(self):
        return u"< UserIndicator: for %s >" % self.user.username
# }}}


class IndicatorRecord(models.Model):                        # {{{
    """
    指标记录
    对应某指标某一次的数据记录
    """
    indicator = models.ForeignKey(Indicator, verbose_name=u"化验指标",
            related_name="indicator_records")
    user = models.ForeignKey(User, verbose_name=u"用户",
            related_name="indicator_records")
    # date
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(u"更新时间",
            auto_now_add=True, auto_now=True)
    # data
    date = models.DateField(u"化验日期")
    # TODO: limit_choices_to
    unit = models.ForeignKey("Unit", verbose_name=u"数据单位",
            related_name="indicator_records", null=True, blank=True)
    value = models.CharField(u"指标数据值", max_length=30,
            blank=True)
    val_min = models.FloatField(u"数据范围下限",
            null=True, blank=True)
    val_max = models.FloatField(u"数据范围上限",
            null=True, blank=True)
    notes = models.TextField(u"记录说明", blank=True)

    class Meta:
        verbose_name_plural = u"指标数据记录"
        ordering = ['indicator__id', 'date', 'created_at']

    def __unicode__(self):
        return u"< IndicatorRecord: #%s; %s, %s, %s >" % (self.id,
                self.user.username, self.indicator.name, self.date)

    def get_absolute_url(self):
        return reverse('show_record',
                kwargs={'pk': self.id})

    def save(self, **kwargs):
        if self.is_valid() and self.check_confine():
            super(IndicatorRecord, self).save(**kwargs)
        else:
            raise ValueError(u'您输入的数据不符合要求')

    def is_valid(self, **kwargs):                           # {{{
        """验证输入数据是否合法"""
        # check if exists record for the date
        qs = IndicatorRecord.objects.filter(indicator=self.indicator,
                date=self.date)
        if qs and qs[0].id != self.id:
            raise ValueError(u'date="%s" 该日期已经存在记录' % self.date)
            return False
        # check dataType
        if self.indicator.dataType == self.indicator.INTEGER_TYPE:
            # 整数型
            try:
                value = int(self.value)
                return True
            except ValueError:
                raise ValueError(u'您提交的指标数据类型不正确')
                return False
        elif self.indicator.dataType == self.indicator.FLOAT_TYPE:
            # 浮点型
            if not self.unit:
                raise ValueError(u'未填写单位')
                return False
            try:
                value = float(self.value)
                return True
            except ValueError:
                raise ValueError(u'value 数据类型不正确')
                return False
        elif self.indicator.dataType == self.indicator.RANGE_TYPE:
            # 范围型
            if not self.unit:
                raise ValueError(u'未填写单位')
                return False
            if (self.val_max is None) or (self.val_min is None):
                raise ValueError(u'val_max 或 val_min 未填写')
                return False
            if (self.val_max <= self.val_min):
                raise ValueError(u'val_max <= val_min')
                return False
            return True
        elif self.indicator.dataType == self.indicator.FLOAT_RANGE_TYPE:
            # 定值/范围型 (浮点定值优先)
            if not self.unit:
                raise ValueError(u'未填写单位')
                return False
            if self.value:
                # 定值
                try:
                    value = float(self.value)
                    return True
                except ValueError:
                    raise ValueError(u'value 数据类型不正确')
                    return False
            elif (self.val_max is not None) and (self.val_min is not None):
                # 范围值
                if (self.val_max <= self.val_min):
                    raise ValueError(u'val_max <= val_min')
                    return False
                else:
                    return True
            else:
                raise ValueError(u'您提交的指标数据不符合要求')
                return False
        elif self.indicator.dataType == self.indicator.PM_TYPE:
            # +/- 型，无单位要求
            if (len(self.value) == 1) and (self.value in [u'+', u'-']):
                return True
            else:
                raise ValueError(u'value 只接受 "+" 或 "-"')
                return False
        ## TODO: RADIO_TYPE, CHECKBOX_TYPE
        elif self.indicator.dataType in [self.indicator.RADIO_TYPE,
                self.indicator.CHECKBOX_TYPE]:
            raise ValueError(u'RADIO_TYPE, CHECKBOX_TYPE 验证未实现')
            return False
        else:
            raise ValueError(u'指标数据类型不合法')
            return False
    # }}}

    def check_confine(self, **kwargs):                      # {{{
        """
        check if the record data within the related confine:
        math_min <= value <= math_max

        NOTE: convert record data to 'standard unit' before comparison
        """
        sind = self.indicator
        # check
        if sind.dataType in [sind.FLOAT_TYPE, sind.RANGE_TYPE,
                sind.FLOAT_RANGE_TYPE]:
            # unit relation
            unit_rel = self.unit.relation
            v = sympy.symbols('v')
            rel_sym = sympy.sympify(unit_rel)
            # error message
            errmsg = u"'%s' 求值错误，请检查只含有变量 'v'" % unit_rel
            # check InnateConfine for the Indicator first
            if not sind.check_confine():
                return False
            # InnateConfine is ok
            sic = sind.innate_confine
            # value
            if self.value:
                try:
                    value = float(self.value)
                except ValueError:
                    print u'ERROR: value="%s" cannot convert to float'\
                            % self.value
                    return False
                # 'value' unit conversion
                try:
                    value_std = float(rel_sym.evalf(subs={v: value}))
                except ValueError:
                    print errmsg
                    raise ValueError(errmsg)
                if (value_std < sic.math_min) or (
                        value_std > sic.math_max):
                    print u'ERROR: value(std) < math_min or value(std) > math_max'
                    return False
            # val_max
            if self.val_max is not None:
                # unit conversion
                try:
                    val_max_std = float(rel_sym.evalf(
                        subs={v: self.val_max}))
                except ValueError:
                    print errmsg
                    raise ValueError(errmsg)
                if (val_max_std <= sic.math_min) or (
                        val_max_std > sic.math_max):
                    print u'ERROR: val_max(std) <= math_min or val_max(std) > math_max'
                    return False
            # val_min
            if self.val_min is not None:
                try:
                    val_min_std = float(rel_sym.evalf(
                        subs={v: self.val_min}))
                except ValueError:
                    print errmsg
                    raise ValueError(errmsg)
                if (val_min_std < sic.math_min) or (
                        val_min_std >= sic.math_max):
                    print u'ERROR: val_min(std) < math_min or val_min(std) >= math_max'
                    return False
            # check finished
            return True
        else:
            # INTEGER_TYPE or PM_TYPE
            return True

    # }}}

    def get_data(self, **kwargs):                           # {{{
        """
        get the record data
        in unit originally filled by the user
        """
        # check the indicator.dataType
        sind = self.indicator
        if sind.dataType in [sind.FLOAT_TYPE, sind.RANGE_TYPE,
                sind.FLOAT_RANGE_TYPE]:
            # self.value
            if self.value:
                value = float(self.value)
            else:
                value = None
            # self.val_max
            if self.val_max:
                val_max = self.val_max
            else:
                val_max = None
            # self.val_min
            if self.val_min:
                val_min = self.val_min
            else:
                val_min = None
            # output data
            data = {
                'id': self.id,
                'date': self.date.isoformat(),
                'value': value,
                'val_max': val_max,
                'val_min': val_min,
                'unit': self.unit.dump(),
                'notes': self.notes,
                'record_histories_id': [rh.id
                    for rh in self.record_histories.all()],
            }
        else:
            data = {
                'id': self.id,
                'date': self.date.isoformat(),
                'value': self.value,
                'val_max': self.val_max,
                'val_min': self.val_min,
                'unit': {},
                'notes': self.notes,
                'record_histories_id': [rh.id
                    for rh in self.record_histories.all()],
            }
        return data
    # }}}

    def get_data_std(self, **kwargs):                       # {{{
        """
        get the record data in 'standard unit'
        """
        # check the indicator.dataType
        sind = self.indicator
        if sind.dataType in [sind.FLOAT_TYPE, sind.RANGE_TYPE,
                sind.FLOAT_RANGE_TYPE]:
            # check if self.unit standard
            if self.unit.standard:
                return self.get_data(**kwargs)
            # check if specified 'standard unit' for this indicator
            elif sind.check_unit():
                # unit relation
                std_unit = sind.get_unit(type="standard")[0]
                unit_rel = self.unit.relation
                v = sympy.symbols('v')
                rel_sym = sympy.sympify(unit_rel)
                # error message
                errmsg = u"'%s' 求值错误，请检查只含有变量 'v'" % unit_rel
                # self.value
                if self.value:
                    value = float(self.value)
                    try:
                        value_std = float(rel_sym.evalf(
                            subs={v: value}))
                    except ValueError:
                        print errmsg
                        raise ValueError(errmsg)
                else:
                    value_std = None
                # self.val_max
                if self.val_max:
                    val_max = self.val_max
                    try:
                        val_max_std = float(rel_sym.evalf(
                            subs={v: val_max}))
                    except ValueError:
                        print errmsg
                        raise ValueError(errmsg)
                else:
                    val_max_std = None
                # self.val_min
                if self.val_min:
                    val_min = self.val_min
                    try:
                        val_min_std = float(rel_sym.evalf(
                            subs={v: val_min}))
                    except ValueError:
                        print errmsg
                        raise ValueError(errmsg)
                else:
                    val_min_std = None
                # output data
                data_std = {
                    'id': self.id,
                    'date': self.date.isoformat(),
                    'value': value_std,
                    'val_max': val_max_std,
                    'val_min': val_min_std,
                    'unit': std_unit.dump(),
                    'notes': self.notes,
                    'record_histories_id': [rh.id
                        for rh in self.record_histories.all()],
                }
                return data_std
            else:
                print u"id=%s Indicator 尚未指定标准单位" % sind.id
                return {}
        else:
            return self.get_data(**kwargs)
    # }}}

    def is_normal(self, **kwargs):                          # {{{
        """
        compare the given data with the indicator confines.

        if the data within the confines, then return 'True',
        which suggests the indicator is normal.
        if the data out of the confines, then return 'False'.

        * return 'None' if there are other problems.
        """
        sind = self.indicator
        # 先检查 Unit 和 InnateConfine 是否已经正确指定
        if not sind.is_ready():
            print u"ERROR: Indicator id=%s NOT ready yet" % sind.id
            return None
        sic = sind.innate_confine
        # 获取以标准单位为单位的数据
        data_std = self.get_data_std()
        # 根据数据类型判断是否处于正常情况
        if sind.dataType == sind.INTEGER_TYPE:
            # 整数型
            value = int(data_std['value'])
            val_norm = int(sic.val_norm)
            # XXX: modify accordingly
            if value == val_norm:
                return True
            else:
                return False
        elif sind.dataType == sind.FLOAT_TYPE:
            # 浮点型
            value = data_std['value']
            human_max = sic.human_max
            human_min = sic.human_min
            if (value <= human_max) and (value >= human_min):
                return True
            else:
                return False
        elif sind.dataType == sind.RANGE_TYPE:
            # 范围型
            val_max = data_std['val_max']
            val_min = data_std['val_min']
            human_max = sic.human_max
            human_min = sic.human_min
            if (val_max <= human_max) and (val_min >= human_min):
                return True
            else:
                return False
        elif sind.dataType == sind.FLOAT_RANGE_TYPE:
            # 浮点型/范围型
            if self.value:
                value = float(data_std['value'])
                human_max = sic.human_max
                human_min = sic.human_min
                if (value <= human_max) and (value >= human_min):
                    return True
                else:
                    return False
            elif self.val_max and self.val_min:
                # 范围值
                val_max = data_std['val_max']
                val_min = data_std['val_min']
                human_max = sic.human_max
                human_min = sic.human_min
                if (val_max <= human_max) and (val_min >= human_min):
                    return True
                else:
                    return False
            else:
                print u'数据类型错误'
                raise ValueError(u'数据类型错误')
                return None
        elif sind.dataType == sind.PM_TYPE:
            # 阴阳(+/-)型
            value = data_std['value']
            val_norm = sic.val_norm
            if value == val_norm:
                return True
            else:
                return False
        elif sind.dataType in [sind.RADIO_TYPE, sind.CHECKBOX_TYPE]:
            print u'RADIO_TYPE, CHECKBOX_TYPE 验证未实现'
            raise ValueError(u'RADIO_TYPE, CHECKBOX_TYPE 验证未实现')
            return None
        else:
            print u'数据类型不合法'
            raise ValueError(u'数据类型不合法')
            return None
    # }}}

    def dump(self, **kwargs):
        # check if the indicator needs unit
        if self.unit:
            unit_id = self.unit.id
        else:
            unit_id = None
        # dump
        dump_data = {
            'id': self.id,
            'indicator_id': self.indicator.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'date': self.date.isoformat(),
            'unit_id': unit_id,
            'value': self.value,
            'val_min': self.val_min,
            'val_max': self.val_max,
            'notes': self.notes,
            'record_histories_id': [rh.id
                for rh in self.record_histories.all()],
        }
        return dump_data
# }}}


class RecordHistory(models.Model):                          # {{{
    """
    指标记录 IndicatorRecord 的历史数据和对应的修改原因
    """
    indicatorRecord = models.ForeignKey("IndicatorRecord",
            verbose_name=u"指标数据记录",
            related_name="record_histories")
    # modification datetime
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    # modification reason
    reason = models.TextField(u"修改原因")
    # original data before modification
    date_bak = models.DateField(u"原化验日期", blank=True,
            editable=False)
    unit_bak = models.ForeignKey("Unit", verbose_name=u"原数据单位",
            related_name="record_histories",
            null=True, blank=True, editable=False)
    value_bak = models.CharField(u"原指标数据值", max_length=30,
            blank=True, editable=False)
    val_min_bak = models.FloatField(u"原数据范围下限",
            null=True, blank=True, editable=False)
    val_max_bak = models.FloatField(u"原数据范围上限",
            null=True, blank=True, editable=False)
    notes_bak = models.TextField(u"原记录说明", blank=True,
            editable=False)

    class Meta:
        verbose_name_plural = u"记录修改历史"
        ordering = ['indicatorRecord__id', 'created_at']

    def __unicode__(self):
        return u"< RecordHistory: #%s, for Record #%s, %s >"\
                % (self.id, self.indicatorRecord.id, self.created_at)

    def save(self, **kwargs):
        sr = self.indicatorRecord
        # get history data from *not-saved* IndicatorRecord
        self.date_bak = sr.date
        self.unit_bak = sr.unit
        self.value_bak = sr.value
        self.val_min_bak = sr.val_min
        self.val_max_bak = sr.val_max
        self.notes_bak = sr.notes
        # save
        super(RecordHistory, self).save(**kwargs)

    def dump(self, **kwargs):
        # check 'unit_bak'
        if self.unit_bak:
            unit_bak_id = self.unit_bak.id
        else:
            unit_bak_id = None
        # dump
        dump_data = {
            'id': self.id,
            'indicatorRecord_id': self.indicatorRecord.id,
            'created_at': self.created_at.isoformat(),
            'reason': self.reason,
            'date_bak': self.date_bak.isoformat(),
            'unit_bak_id': unit_bak_id,
            'value_bak': self.value_bak,
            'val_min_bak': self.val_min_bak,
            'val_max_bak': self.val_max_bak,
            'notes_bak': self.notes_bak,
        }
        return dump_data
# }}}


class Unit(models.Model):                                   # {{{
    """
    指标单位
    是否为标准单位，其他单位与标准单位的换算关系
    """
    # related to the `indicator'
    indicator = models.ForeignKey(Indicator, verbose_name=u"指标",
            related_name="units")
    name = models.CharField(u"单位名称", max_length=50)
    symbol = models.CharField(u"单位符号", max_length=50)
    standard = models.BooleanField(u"是否标准单位", default=False)
    # conversion relation
    relation = models.CharField(u"与标准单位的映射",
            help_text=u"value (std_unit) = f(v)",
            max_length=100, blank=True)
    description = models.TextField(u"单位描述", blank=True)
    # 记录添加的用户，用户只能修改自己添加的对象
    addByUser = models.ForeignKey(User, verbose_name=u"添加的用户",
            related_name="units")

    class Meta:
        verbose_name_plural = u"单位"

    def __unicode__(self):
        if self.standard:
            _std = ' (*)'
        else:
            _std = ''
        return u"< Unit: %s%s for %s, addBy %s >" % (self.name,
                _std, self.indicator.name, self.addByUser.username)

    def is_valid(self):
        if self.standard:
            std_unit_list = self.indicator.get_unit(type="standard")
            if std_unit_list:
                std_unit = std_unit_list[0]
                if self.id == std_unit.id:
                    return True
                else:
                    print u"该指标已经指定了标准单位"
                    raise ValueError(u"该指标已经指定了标准单位")
                    return False
            else:
                return True
        else:
            if (not self.relation):
                print u"单位映射关系未填写"
                raise ValueError(u"单位映射关系未填写")
                return False
            else:
                try:
                    fsym = sympy.sympify(self.relation)
                    return True
                except SympifyError:
                    print u"'%s' 不是合法的算术表达式" % self.relation
                    raise ValueError(u"'%s' 不是合法的算术表达式"\
                            % self.relation)
                    return False

    def save(self, **kwargs):
        if self.standard:
            self.relation = "v"
        if self.is_valid():
            super(Unit, self).save(**kwargs)

    def dump(self, **kwargs):
        dump_data = {
            'id': self.id,
            'indicator_id': self.indicator.id,
            'name': self.name,
            'symbol': self.symbol,
            'standard': self.standard,
            'relation': self.relation,
            'addByUser_id': self.addByUser.id,
        }
        return dump_data
# }}}


class InnateConfine(models.Model):                          # {{{
    """
    指标数据范围
    数学可能值范围，人体正常值范围

    注意：
    如果数据类型需要单位，则必须使用"标准单位"；
    IndicatorRecord.is_normal() 方法需要如此；
    因为 标准单位 到 其他单位 的换算没有实现。
    """
    # indicator
    indicator = models.OneToOneField("Indicator",
            verbose_name=u"指标", related_name="innate_confine")
    # unit
    # TODO: limit_choices_to
    unit = models.ForeignKey("Unit", related_name="innate_confines",
            verbose_name=u"单位", null=True, blank=True)
    # normal value (for INTEGER_TYPE, PM_TYPE)
    val_norm = models.CharField(u"正常值", max_length=30, blank=True,
            help_text=u'填写"整数型","阴阳(+/-)型数据"')
    # normal range
    human_min = models.FloatField(u"人体正常值下限",
            null=True, blank=True)
    human_max = models.FloatField(u"人体正常值上限",
            null=True, blank=True)
    # possbile range
    math_min = models.FloatField(u"数学可能值下限",
            null=True, blank=True)
    math_max = models.FloatField(u"数学可能值上限",
            null=True, blank=True)
    # description or notes
    description = models.TextField(u"描述", blank=True)
    # 记录添加的用户，用户只能修改自己添加的对象
    addByUser = models.ForeignKey(User, verbose_name=u"添加的用户",
            related_name="innate_confines")

    class Meta:
        verbose_name_plural = u"固有数值范围"

    def __unicode__(self):
        return u"< InnateConfine: for %s, addBy %s >"\
                % (self.indicator.name, self.addByUser.username)

    def save(self, **kwargs):
        """
        check the data before save
        """
        if self.is_valid():
            super(InnateConfine, self).save(**kwargs)
        else:
            print u"您填写的数据不符合要求，请检查"
            return self

    def is_valid(self):                                     # {{{
        """
        check the validity of data
        """
        sind = self.indicator
        if sind.dataType in [sind.FLOAT_TYPE, sind.RANGE_TYPE,
                sind.FLOAT_RANGE_TYPE]:
            # check unit
            if not (self.unit and self.unit.standard):
                raise ValueError(u'单位未填写/不是标准单位')
                return False
            if (self.human_max is None) or (self.human_min is None):
                raise ValueError(u'Error: human_max 或 human_min 未填写')
                return False
            if not (self.human_max > self.human_min):
                raise ValueError(u'Error: human_max <= human_min')
                return False
            # check 'math_max' and 'math_min'
            if (self.math_max is None) or (self.math_min is None):
                raise ValueError(u'Error: math_max 或 math_min 未填写')
                return False
            if not (self.math_max > self.math_min):
                raise ValueError(u'Error: math_max <= math_min')
                return False
            # compare 'human*' and 'math*'
            if (self.human_max > self.math_max) or (
                    self.human_min < self.math_min):
                raise ValueError(u'Error: human_max>math_max / human_min<math_min')
                return False
            # check finished
            return True
        elif sind.dataType == sind.INTEGER_TYPE:
            # 整数型
            try:
                val_norm = int(self.val_norm)
                return True
            except ValueError:
                raise ValueError(u'val_norm="%s" 不是整数型值'
                        % self.val_norm)
                return False
        elif sind.dataType == sind.PM_TYPE:
            # 阴阳(+/-)型
            if (len(self.val_norm) == 1) and (
                    self.val_norm in [u'+', u'-']):
                return True
            else:
                raise ValueError(u'value 只接受 "+" 或 "-"')
                return False
        ## TODO: RADIO_TYPE, CHECKBOX_TYPE
        elif sind.dataType in [sind.RADIO_TYPE, sind.CHECKBOX_TYPE]:
            raise ValueError(u'RADIO_TYPE, CHECKBOX_TYPE 验证未实现')
            return False
        else:
            raise ValueError(u'数据不符合要求')
            return False
    # }}}

    def dump(self, **kwargs):
        # check unit, if the indicator not need unit, then return {}
        if self.unit:
            unit_dump = self.unit.dump()
        else:
            unit_dump = {}
        # dump
        dump_data = {
            'id': self.id,
            'indicator_id': self.indicator.id,
            'unit': unit_dump,
            'val_norm': self.val_norm,
            'human_min': self.human_min,
            'human_max': self.human_max,
            'math_min': self.math_min,
            'math_max': self.math_max,
            'addByUser_id': self.addByUser.id,
        }
        return dump_data
# }}}


class StatisticalConfine(models.Model):                     # {{{

    deviation_ceiling = models.FloatField(u"统计偏差范围上限", null=True, blank=True)
    deviation_floor   = models.FloatField(u"统计偏差范围限", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"统计数值范围"

    def __unicode__(self):
        return "< StatisticalConfine: %s >" % self.id
# }}}


#class UnitLabSheet(models.Model):                           # {{{
#
#    equipment = models.CharField(u"化验设备", max_length=100, null=True, blank= True)
#    #figure = models.OneToOneField("figure.Figure", verbose_name=u"图片", related_name="unitlabsheet")
#    unit_standard = models.ForeignKey("UnitStandard", verbose_name = u"单位标准", related_name="unit_lab_sheets", null=True, blank=True)
#
#    class Meta:
#        verbose_name_plural = u"标准化验单"
#
#    def __unicode__(self):
#        return "< UnitLabSheet: %s >" % self.id
## }}}


#class ReviseReason(models.Model):                           # {{{
#    """
#    记录 IndicatorRecord 数据修改原因
#    医学数据重要且要求准确，不可随意修改
#    ReviseReason 添加后不允许再修改？
#    """
#    # TODO: 中文支持
#    content = models.TextField(u"内容")
#    created_at = models.DateTimeField(u"创建时间",
#            editable=False, auto_now_add=True)
#    user = models.ForeignKey(User, verbose_name=u"用户")
#
#    class Meta:
#        verbose_name_plural=u"指标记录修改原因"
#
#    def __unicode__(self):
#        return u"< ReviseReason: %s, %s >" % (self.id,
#                self.user.username)
#
#    def dump(self, **kwargs):
#        dump_data = {
#            'id': self.id,
#            'content': self.content,
#            'created_at': self.created_at.isoformat(),
#            'user_id': self.user.id,
#        }
#        return dump_data
## }}}


class RelatedIndicator(models.Model):                       # {{{
    """
    记录 blog/annotation 与哪些 indicator 关联，
    以及关联的权重。

    用于为用户推荐可以关注的指标。
    """
    # indicator
    indicator = models.ForeignKey("Indicator",
            related_name="related_indicators",
            verbose_name=u"待关联指标")
    # type of related object
    ANNOTATION_TYPE = 'AN'
    BLOG_TYPE = 'BL'
    OBJECT_TYPES = (
        (ANNOTATION_TYPE, '文章注释'),
        (BLOG_TYPE, '文章'),
    )
    objectType = models.CharField(u"待关联目标类型", max_length=2,
            choices=OBJECT_TYPES)
    # objects
    annotation = models.ForeignKey("sciblog.BlogAnnotation",
            related_name="related_indicators",
            verbose_name=u"待关联文章注释", null=True, blank=True)
    blog = models.ForeignKey("sciblog.SciBlog",
            related_name="related_indicators",
            verbose_name=u"待关联文章", null=True, blank=True)
    # weight
    weight = models.FloatField(u"权重", help_text=u"范围: 0-10")
    # datetime
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(u"更新时间",
            auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name_plural = u"指标关联信息"
        ordering = ['objectType']

    def __unicode__(self):
        if self.objectType == self.ANNOTATION_TYPE:
            info = 'Annotation #%s' % self.annotation.id
        elif self.objectType == self.BLOG_TYPE:
            info = 'Blog #%s' % self.blog.id
        else:
            info = '%s' % self.objectType
        return u"< RelatedIndicator: %s -> %s >"\
                % (info, self.indicator.name)

    def save(self, **kwargs):
        if self.is_valid():
            if self.objectType == self.ANNOTATION_TYPE:
                self.blog = None
            if self.objectType == self.BLOG_TYPE:
                self.annotation = None
            # save
            super(RelatedIndicator, self).save(**kwargs)
        else:
            return self

    def is_valid(self, **kwargs):                           # {{{
        """
        annotation/blog must be consistent with objectType
        """
        # check objectType
        if self.objectType == self.ANNOTATION_TYPE:
            if not self.annotation:
                raise ValueError(u"Error: annotation 未填写")
                return False
        elif self.objectType == self.BLOG_TYPE:
            if not self.blog:
                raise ValueError(u"Error: blog 未填写")
                return False
        else:
            raise ValueError(u"Error: objectType 不合法")
            return False
        # check weight range
        if (self.weight < 0.0) or (self.weight > 10.0):
            raise ValueError(u"Error: weight < 0.0 / weight > 10.0")
            return False
        # finished
        return True
    # }}}

    def dump(self, **kwargs):
        # annotation_id
        if self.annotation:
            annotation_id = self.annotation.id
        else:
            annotation_id = None
        # blog_id
        if self.blog:
            blog_id = self.blog.id
        else:
            blog_id = None
        # dump data
        dump_data = {
            'id': self.id,
            'indicator_id': self.indicator.id,
            'objectType': self.objectType,
            'annotation_id': annotation_id,
            'blog_id': blog_id,
            'weight': self.weight,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        return dump_data
# }}}



admin.site.register([
                     IndicatorCategory,
                     Indicator,
                     UserIndicator,
                     IndicatorRecord,
                     RecordHistory,
                     Unit,
                     InnateConfine,
                     StatisticalConfine,
                     #UnitLabSheet,
                     #ReviseReason,
                     RelatedIndicator,
                    ])

# vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=python: #
