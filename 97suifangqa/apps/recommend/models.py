# -*- coding: utf-8 -*-

"""
models for apps/recommend
"""


from django.db import models
from django.contrib import admin

from utils.tools import format_float

import re


class TreatResponse(models.Model):                           # {{{
    """
    治疗反应/结果的描述，以及结果的价值/权重
    """
    name = models.CharField(u"名称", max_length=100)
    description = models.TextField(u"详细描述", blank=True)
    weight = models.FloatField(u"权重", help_text=u"范围：0-10")
    # datetime
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(u"更新时间",
            auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name_plural = u"治疗反应"

    def __unicode__(self):
        return u"< TreatResponse: %s >" % self.name

    def save(self, **kwargs):
        if self.is_valid():
            super(TreatResponse, self).save(**kwargs)
        else:
            return self

    def is_valid(self, **kwargs):
        # check weight range
        if (self.weight < 0.0) or (self.weight > 10.0):
            print u"Error: weight < 0.0 / weight > 10.0"
            raise ValueError(u"Error: weight<0.0 / weight>10.0")
            return False
        #
        return True

    def dump(self, **kwargs):
        dump_data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
        }
        return dump_data
# }}}


class ResearchIndicator(models.Model):                      # {{{
    """
    model to record the indicators which researched in the paper
    """
    MEAN_TYPE = 'MEAN'
    SCOPE_TYPE = 'SCOP'
    KIND_TYPE = 'KIND'
    DATA_TYPES = (
        (MEAN_TYPE, u'平均值'),
        (SCOPE_TYPE, u'范围'),
        (KIND_TYPE, u'种类'),
    )
    blog = models.ForeignKey("sciblog.SciBlog",
            related_name="research_indicators",
            verbose_name=u"待关联文章")
    indicator = models.ForeignKey("indicator.Indicator",
            related_name="research_indicators",
            verbose_name=u"待关联指标")
    dataType = models.CharField(u"指标值类型", max_length=4,
            choices=DATA_TYPES)
    # datetime
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(u"更新时间",
            auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name_plural = u"研究指标信息"
        ordering = ['blog__id', 'indicator__id']

    def __unicode__(self):
        # cut down the length of title
        blog_title = self.blog.title[:10]
        return u"< ResearchIndicator: %s -> %s (type %s) >" % (
                blog_title, self.indicator.name, self.dataType)

    def save(self, **kwargs):
        if self.is_valid():
            super(ResearchIndicator, self).save(**kwargs)
        else:
            return self

    def is_valid(self, **kwargs):                           # {{{
        # check dataType, which should be consistent with the
        # dataType of the related indicator
        ind_obj = self.indicator
        ind_dataType = ind_obj.dataType
        if self.dataType == self.MEAN_TYPE:
            if ind_dataType not in [ind_obj.FLOAT_TYPE, ind_obj.FLOAT_RANGE_TYPE]:
                raise ValueError(u"Error: dataType与Indicator不符")
                return False
        elif self.dataType == self.SCOPE_TYPE:
            if ind_dataType not in [ind_obj.RANGE_TYPE, ind_obj.FLOAT_RANGE_TYPE, ind_obj.FLOAT_TYPE]:
                raise ValueError(u"Error: dataType与Indicator不符")
                return False
        elif self.dataType == self.KIND_TYPE:
            if ind_dataType in [ind_obj.FLOAT_TYPE,
                    ind_obj.RANGE_TYPE, ind_obj.FLOAT_RANGE_TYPE]:
                raise ValueError(u"Error: dataType与Indicator不符")
                return False
        else:
            raise ValueError(u"Error: unknown dataType")
            return False
        #
        return True
    # }}}

    def dump(self, **kwargs):
        dump_data = {
            'id': self.id,
            'blog_id': self.blog.id,
            'indicator_id': self.indicator.id,
            'indicator_name': self.indicator.name,
            'dataType': self.dataType,
        }
        return dump_data
# }}}


# class ResearchCombination(models.Model):                    # {{{
#     """
#     记录文章研究的有效的指标组合
#     """
#     blog = models.ForeignKey("sciblog.SciBlog",
#             related_name="research_combinations",
#             verbose_name=u"待关联文章")
#     combination = models.ManyToManyField("indicator.Indicator",
#             related_name="research_combinations",
#             verbose_name=u"研究指标组合")
#     # datetime
#     created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
#     updated_at = models.DateTimeField(u"更新时间",
#             auto_now_add=True, auto_now=True)
# 
#     class Meta:
#         verbose_name_plural = u"研究指标有效组合"
#         ordering = ['blog__id']
# 
#     def __unicode__(self):
#         # cut down the length of title
#         blog_title = self.blog.title[:10]
#         combination = u''
#         for ind in self.combination:
#             combination = combination + ind.name + ", "
#         combination = re.sub(r',\ $', '', combination)
#         return u"< ResearchCombination: %s -> (%s) >" % (
#                 blog_title, combination)
# 
#     def save(self, **kwargs):
#         if self.is_valid():
#             super(ResearchCombination, self).save(**kwargs)
#         else:
#             return self
# 
#     def is_valid(self):
#         """
#         These M2M indicators must have related to the blog
#         """
#         related_indicators = [ri.indicator
#                 for ri in self.blog.research_indicators.all()]
#         for ind in self.combination:
#             if ind not in related_indicators:
#                 raise ValueError(u"Error: 选择了未关联到该文章的指标")
#                 return False
#         return True
# # }}}


# ResearchAtom {{{
class ResearchAtom(models.Model):
    """
    ???any good name???
    用于记录某篇文章中对某个指标所分的每一个小类的具体信息
    """
    blog = models.ForeignKey("sciblog.SciBlog",
            related_name="research_atoms",
            verbose_name=u"待关联文章")
    researchIndicator = models.ForeignKey("ResearchIndicator",
            related_name="research_atoms",
            verbose_name=u"文章研究指标")
    ## value
    # unit (XXX: only standard unit supported at the moment)
    unit = models.ForeignKey("indicator.Unit",
            null=True, blank=True,
            related_name="research_atoms", verbose_name=u"单位")
    # dataType: MEAN
    mean = models.FloatField(u"平均值", null=True, blank=True)
    sd = models.FloatField(u"标准值", null=True, blank=True)
    # dataType: SCOP
    scope_min = models.FloatField(u"范围下限", null=True, blank=True)
    scope_max = models.FloatField(u"范围上限", null=True, blank=True)
    # dataType: KIND
    kind = models.ForeignKey("indicator.ValueKind",
            null=True, blank=True,
            related_name="research_atoms", verbose_name=u"种类")
    ## datetime
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(u"更新时间",
            auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name_plural = u"研究指标原子类"
        ordering = ['blog__id', 'researchIndicator__id']

    def __unicode__(self):
        return u'< ResearchAtom: #%s %s >' % (self.id, self.display())

    def save(self, **kwargs):
        if self.is_valid():
            super(ResearchAtom, self).save(**kwargs)
        else:
            return self

    def is_valid(self, **kwargs):                           # {{{
        """
        The blog here must be consistent with the blog related to
        the researchIndicator
        """
        ri_obj = self.researchIndicator
        dataType = ri_obj.dataType
        # confine
        ind_obj = ri_obj.indicator
        if ind_obj.check_confine():
            confine = ind_obj.get_confine()
        else:
            raise ValueError(u"Error: 该指标未指定InnateConfine")
            return False
        # check blog id first
        if self.blog.id != ri_obj.blog.id:
            raise ValueError(u"Error: 关联blog错误")
            return False
        # check dataType and confine
        if dataType == ri_obj.MEAN_TYPE:
            if not (self.unit and self.unit.standard):
                raise ValueError(u"Error: 单位未填写/不是标准单位")
                return False
            if ((self.mean is None) or (self.sd is None)):
                raise ValueError(u"Error: 平均值/标准差未填写")
                return False
            # check with confine
            # XXX: only check 'mean' at the moment; 'sd' may also needed
            if (self.mean < confine['math_min']) or (
                    self.mean > confine['math_max']):
                raise ValueError(u"Error: 平均值超出允许范围")
                return False
        elif dataType == ri_obj.SCOPE_TYPE:
            if not (self.unit and self.unit.standard):
                raise ValueError(u"Error: 单位未填写/不是标准单位")
                return False
            if ((self.scope_min is None) or (self.scope_max is None)):
                raise ValueError(u"Error: 范围下限/上限未填写")
                return False
            if (self.scope_min >= self.scope_max):
                raise ValueError(u"Error: scope_min>=scope_max")
                return False
            # check confine
            if (self.scope_min < confine['math_min']) or (
                    self.scope_max > confine['math_max']):
                raise ValueError(u"Error: scope_min/scope_max 超出允许范围")
                return False
        elif dataType == ri_obj.KIND_TYPE:
            if not self.kind:
                raise ValueError(u"Error: 未选择种类")
                return False
        else:
            raise ValueError(u"Error: unknown dataType")
            return False
        #
        return True
    # }}}

    def get_value(self, **kwargs):                          # {{{
        ri_obj = self.researchIndicator
        dataType = ri_obj.dataType
        value = {
            'id': self.id,
            'dataType': dataType,
            'blog_id': self.blog.id,
        }
        if dataType == ri_obj.MEAN_TYPE:
            value['mean'] = self.mean
            value['sd'] = self.sd
            value['unit'] = self.unit.dump()
        elif dataType == ri_obj.SCOPE_TYPE:
            value['scope_min'] = self.scope_min
            value['scope_max'] = self.scope_max
            value['unit'] = self.unit.dump()
        elif dataType == ri_obj.KIND_TYPE:
            value['kind'] = self.kind.dump()
        else:
            value['error'] = True
        return value
    # }}}

    def display(self, **kwargs):
        """
        generate the display string for front page
        """
        ri_obj = self.researchIndicator
        ind_name = ri_obj.indicator.name
        dataType = ri_obj.dataType
        if dataType == ri_obj.MEAN_TYPE:
            value = '%sSD%s' % (format_float(self.mean), self.sd)
        elif dataType == ri_obj.SCOPE_TYPE:
            value = '%s~%s' % (format_float(self.scope_min),
                    format_float(self.scope_max))
        elif dataType == ri_obj.KIND_TYPE:
            value = '%s' % (self.kind.name)
        else:
            value = 'UNKNOWN'
        disp_str = u'%s(%s|%s)' % (ind_name, dataType, value)
        return disp_str
# }}}


# ResearchConfig {{{
class ResearchConfig(models.Model):
    """
    记录某篇文章所研究的某一个具体的组合（哪几个指标的具体值）
    的治疗结果等信息
    """
    blog = models.ForeignKey("sciblog.SciBlog",
            related_name="research_configs",
            verbose_name=u"待关联文章")
    researchAtoms = models.ManyToManyField("ResearchAtom",
            related_name="research_configs",
            verbose_name=u"研究指标值组合")
    treatResponse = models.ForeignKey("TreatResponse",
            related_name="research_configs",
            verbose_name=u"治疗反应")
    weight = models.FloatField(u"权重", help_text=u"范围：0-10")
    # datetime
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(u"更新时间",
            auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name_plural = u"研究指标值组合信息"
        ordering = ['blog__id']

    def __unicode__(self):
        # XXX
        info = ''
        for atom in self.researchAtoms.all():
            info = '%s%s,' % (info, atom.id)
        info = re.sub(r',\s*$', '', info)
        return u'< ResearchConfig: #%s (Atoms: %s) -> %s >' % (
                self.id, info, self.blog.title[:10])

    def save(self, **kwargs):
        if self.is_valid():
            super(ResearchConfig, self).save(**kwargs)
        else:
            return self

    def is_valid(self):
        """
        The blog here must be consistent with the blog related to
        the researchAtoms
        """
        # check weight range
        if (self.weight < 0.0) or (self.weight > 10.0):
            raise ValueError(u"Error: weight<0.0 / weight>10.0")
            return False
        #### check blog ####
        ## Error: needs to have a value for field "researchconfig" before this many-to-many relationship can be used.
        #for atom in self.researchAtoms.all():
        #    if atom.blog.id != self.blog.id:
        #        raise ValueError(u"Error: 关联blog错误")
        #        return False
        #### end ####
        return True

    def is_ok(self, **kwargs):
        """
        check this config whether ok or not?
        i.e.: whether the data fields are valid?
        """
        # check atoms
        if not self.researchAtoms.all():
            return False
        # check blog id
        for atom in self.researchAtoms.all():
            if atom.blog.id != self.blog.id:
                raise ValueError(u"Error: 关联blog错误")
                return False
        #
        return True

    def dump(self, **kwargs):
        dump_data = {
            'id': self.id,
            'blog_id': self.blog.id,
            'researchAtoms_id': [atom.id
                for atom in self.researchAtoms.all()],
            'treatResponse_id': self.treatResponse.id,
            'weight': self.weight,
        }
        return dump_data
# }}}


# admin
admin.site.register([
    TreatResponse,
    ResearchIndicator,
    #ResearchCombination,
    ResearchAtom,
    ResearchConfig,
])

