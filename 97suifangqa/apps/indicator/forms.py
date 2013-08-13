# -*- coding: utf-8 -*-

"""
forms for apps/indicator
"""

from django import forms
from django.utils.translation import ugettext as _

from indicator import models as im

import sympy
from sympy.core.sympify import SympifyError


class IndicatorCategoryForm(forms.ModelForm):               # {{{
    """
    form for 'models.IndicatorCategory'
    """
    class Meta:
        model = im.IndicatorCategory
        exclude = ('addByUser',)
# }}}


class IndicatorForm(forms.ModelForm):                       # {{{
    """
    form for 'models.Indicator'
    """
    class Meta:
        model = im.Indicator
        exclude = ('addByUser',)
# }}}


class UnitForm(forms.ModelForm):                            # {{{
    """
    form for 'models.Unit'
    """
    class Meta:
        model = im.Unit
        exclude = ('addByUser',)

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        # store 'instance_id', for edting instance
        self.instance_id = self.instance.id

    # 'clean_standard()' cannot raise Vali dationError correctly??
    # TODO: clean each field and generate errors accordingly.

    def clean(self):
        cleaned_data = super(UnitForm, self).clean()
        instance_id = self.instance_id
        standard = cleaned_data['standard']
        indicator = cleaned_data['indicator']
        std_unit_list = indicator.get_unit(type="standard")
        relation = cleaned_data.get('relation', u'')
        if standard:
            if std_unit_list and (instance_id != std_unit_list[0].id):
                raise forms.ValidationError(_(u'标准单位已存在'),
                        code='standard')
            cleaned_data['relation'] = u'v'
        else:
            try:
                fsym = sympy.sympify(relation)
            except SympifyError:
                raise forms.ValidationError(_(u'"%(relation)s" 不是合法的表达式'),
                    code='relation_invalid',
                    params={'relation': relation})
        # always return the full collection of cleaned data
        return cleaned_data
# }}}


class InnateConfineForm(forms.ModelForm):                   # {{{
    """
    form for 'models.InnateConfine'
    """
    unit = forms.ModelChoiceField(label=u"标准单位",
            queryset=im.Unit.objects.filter(standard=True))

    class Meta:
        model = im.InnateConfine
        exclude = ('addByUser',)

    def clean(self):                                        # {{{
        """
        check the validity of data
        """
        cleaned_data = super(InnateConfineForm, self).clean()
        indicator = cleaned_data['indicator']
        unit = cleaned_data.get('unit')
        val_norm = cleaned_data.get('val_norm')
        human_max = cleaned_data.get('human_max')
        human_min = cleaned_data.get('human_min')
        math_max = cleaned_data.get('math_max')
        math_min = cleaned_data.get('math_min')
        # check data
        if indicator.dataType in [indicator.FLOAT_TYPE,
                indicator.RANGE_TYPE, indicator.FLOAT_RANGE_TYPE]:
            # check unit
            if not (unit and unit.standard):
                raise forms.ValidationError(_(u'unit 未填写/不是标准单位'),
                        code='unit')
            if (human_max is None) or (human_min is None):
                raise forms.ValidationError(_(u'human_max/human_min 未填写'),
                        code='human_empty')
            if (human_max <= human_min):
                raise forms.ValidationError(_(u'human_max <= human_min'),
                        code='human_relation')
            # check 'math_max' and 'math_min'
            if (math_max is None) or (math_min is None):
                raise forms.ValidationError(_(u'math_max/math_min 未填写'),
                        code='math_empty')
            if (math_max <= math_min):
                raise forms.ValidationError(_(u'math_max <= math_min'),
                        code='math_relation')
            # compare 'human*' and 'math*'
            if (human_max > math_max) or (human_min < math_min):
                raise forms.ValidationError(_(u'Error: human_max>math_max / human_min<math_min'),
                        code='human_math_relation')
            # check finished
        elif indicator.dataType == indicator.INTEGER_TYPE:
            # 整数型
            try:
                val_norm = int(val_norm)
            except ValueError:
                raise ValidationError(_(u'val_norm="%(val_norm)s" 不是整数型值'),
                        code='val_norm_int',
                        params={'val_norm': val_norm})
        elif indicator.dataType == indicator.PM_TYPE:
            # 阴阳(+/-)型
            if (len(val_norm) == 1) and (val_norm in [u'+', u'-']):
                pass
            else:
                raise forms.ValidationError(_(u'val_norm 只接受 "+"/"-"'),
                        code='val_norm_pm')
        ## TODO: RADIO_TYPE, CHECKBOX_TYPE
        elif indicator.dataType in [indicator.RADIO_TYPE,
                indicator.CHECKBOX_TYPE]:
            raise forms.ValidationError(_(u'RADIO_TYPE, CHECKBOX_TYPE 验证未实现'),
                    code='radio_checkbox')
        else:
            raise forms.ValidationError(_(u'数据不符合要求'),
                    code='data_type_invalid')
        # all checks finished
        return cleaned_data
    # }}}
# }}}


class IndicatorRecordForm(forms.ModelForm):                 # {{{
    """
    form for 'models.IndicatorRecord'
    """

    class Meta:
        model = im.IndicatorRecord
        exclude = ('user',)

    def clean(self):                                        # {{{
        cleaned_data = super(IndicatorRecordForm, self).clean()
        # get data
        indicator = cleaned_data['indicator']
        unit = cleaned_data.get('unit')
        _value = cleaned_data.get('value')
        _val_max = cleaned_data.get('val_max')
        _val_min = cleaned_data.get('val_min')
        # check data                                        # {{{
        if indicator.dataType == indicator.INTEGER_TYPE:
            # integer
            try:
                value = int(_value)
            except ValueError:
                raise forms.ValidationError(_(u'value 不是整数类型'),
                        code='value_integer')
        elif indicator.dataType == indicator.FLOAT_TYPE:
            # float
            if not unit:
                raise forms.ValidationError(_(u'unit 未填写'),
                        code='unit_empty')
            try:
                value = float(_value)
            except ValueError:
                raise forms.ValidationError(_(u'value 不是浮点数类型'),
                        code='value_float')
        elif indicator.dataType == indicator.RANGE_TYPE:
            # range
            val_max = _val_max
            val_min = _val_min
            if not unit:
                raise forms.ValidationError(_(u'unit 未填写'),
                        code='unit_empty')
            if (val_max is None) or (val_min is None):
                raise forms.ValidationError(_(u'val_max/val_min 未填写'),
                        code='val_empty')
            if (val_max <= val_min):
                raise forms.ValidationError(_(u'val_max <= val_min'),
                        code='val_relation')
        elif indicator.dataType == indicator.FLOAT_RANGE_TYPE:
            # float/range
            if not unit:
                raise forms.ValidationError(_(u'unit 未填写'),
                        code='unit_empty')
            if value:
                # float (first)
                try:
                    value = float(_value)
                except ValueError:
                    raise forms.ValidationError(_(u'value 不是浮点数类型'),
                            code='value_float')
            elif (val_max is not None) or (val_min is not None):
                # range
                val_max = _val_max
                val_min = _val_min
                if (val_max <= val_min):
                    raise forms.ValidationError(_(u'val_max <= val_min'),
                            code='val_relation')
            else:
                raise forms.ValidationError(_(u'请填写 value 或者 "val_max + val_min"'),
                        code='value_val')
        elif indicator.dataType == indicator.PM_TYPE:
            # +/-
            value = _value
            if (len(value) == 1) and (value in [u'+', u'-']):
                pass
            else:
                raise forms.ValidationError(_(u'value 只接受 "+"/"-"'),
                        code='value_pm')
        elif indicator.dataType in [indicator.RADIO_TYPE,
                indicator.CHECKBOX_TYPE]:
            ## TODO: RADIO_TYPE, CHECKBOX_TYPE
            raise forms.ValidationError(_(u'RADIO_TYPE, CHECKBOX_TYPE 验证未实现'),
                    code='radio_checkbox')
        else:
            raise forms.ValidationError(_(u'数据不符合要求'),
                    code='data_type_invalid')
        # }}}
        # check confine                                     # {{{
        # for [FLOAT_TYPE, RANGE_TYPE, FLOAT_RANGE_TYPE]
        # [INTEGER_TYPE, PM_TYPE] already validated above
        if indicator.dataType in [indicator.FLOAT_TYPE,
                indicator.RANGE_TYPE, indicator.FLOAT_RANGE_TYPE]:
            # check confine if specified for the indicator
            if not indicator.check_confine():
                raise forms.ValidationError(_(u'该指标未指定 InnateConfine'),
                        code='innateconfine')
            # innateconfine ok
            confine = indicator.innate_confine
            human_max = confine.human_max
            human_min = confine.human_min
            math_max = confine.math_max
            math_min = confine.math_min
            # unit conversion
            unit_rel = unit.relation
            v = sympy.symbols('v')
            rel_sym = sympy.sympify(unit_rel)
            # data
            value = _value
            val_max = _val_max
            val_min = _val_min
            # value
            if value:
                try:
                    value = float(value)
                except ValueError:
                    raise forms.ValidationError(_(u'value 不是浮点数类型'),
                            code='value_float')
                # 'value' unit conversion
                try:
                    value_std = float(rel_sym.evalf(subs={v: value}))
                except ValueError:
                    raise forms.ValidationError(_(u'"%s" 求值错误，请检查只有变量"v"' % unit_rel),
                            code='value_evalf')
                if (value_std < math_min) or (value_std > math_max):
                    raise forms.ValidationError(_(u'value(std) < math_min or value(std) > math_max'),
                            code='value_std_relation')
            # val_max
            if val_max is not None:
                # unit conversion
                try:
                    val_max_std = float(rel_sym.evalf(
                        subs={v: val_max}))
                except ValueError:
                    raise forms.ValidationError(_(u'"%s" 求值错误，请检查只有变量"v"' % unit_rel),
                            code='val_max_evalf')
                if (val_max_std <= math_min) or (
                        val_max_std > math_max):
                    raise forms.ValidationError(_(u'val_max(std) <= math_min or val_max(std) > math_max'),
                            code='val_max_std_relation')
            # val_min
            if val_min is not None:
                try:
                    val_min_std = float(rel_sym.evalf(
                        subs={v: val_min}))
                except ValueError:
                    raise forms.ValidationError(_(u'"%s" 求值错误，请检查只有变量"v"' % unit_rel),
                            code='val_min_evalf')
                if (val_min_std < math_min) or (
                        val_min_std >= math_max):
                    raise forms.ValidationError(_(u'val_min(std) < math_min or val_min(std) >= math_max'),
                            code='val_min_std_relation')
        # }}}
        # return cleaned data
        return cleaned_data
    # }}}
# }}}


class RecordHistoryForm(forms.ModelForm):                   # {{{
    """
    form for 'models.RecordHistory'
    """
    class Meta:
        model = im.RecordHistory
        exclude = ('indicatorRecord',)
# }}}


# vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=python.django: #
