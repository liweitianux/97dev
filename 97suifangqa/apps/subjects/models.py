# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin

# Create your models here.
class Sample(models.Model):
    
    life_condition     = models.CharField(u"现状生活状况", max_length=400, blank=True) 
    side_effect_report = models.TextField(u"副作用报告", blank=True)
    treatment_history  = models.ManyToManyField("TreatmentHistory",verbose_name=u"用药历史", related_name="samples", null=True, blank=True)
    resistance_history = models.ForeignKey("ResistanceHistory",verbose_name=u"耐药历史", related_name="samples", null=True, blank=True)
    nation             = models.ManyToManyField("location.Nation", verbose_name=u"国家", related_name="samples", null=True, blank=True)
    gender_statistic   = models.OneToOneField("GenderStatistic", verbose_name=u"性别统计", related_name="samples", null=True, blank=True)
    age                = models.OneToOneField("Age", verbose_name=u"年龄", related_name="samples", null=True, blank=True)
    complexity = models.IntegerField(u"复杂程度")
    
    class Meta:
        verbose_name_plural = u"人群"
        
    def __unicode__(self):
        return "< Sample: %s >" % self.id
        
    
class Age(models.Model):

    average_age         = models.FloatField(u"平均值")
    statistical_confine = models.OneToOneField("indicator.StatisticalConfine", verbose_name=u"统计数值范围", related_name="ages", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"年龄"

    def __unicode__(self):
        return "< Age: %s >" % self.id
    

class GenderStatistic(models.Model):

    male_value  = models.IntegerField(u"男性人数")
    female_vale = models.IntegerField(u"女性人数")

    class Meta:
        verbose_name_plural = u"性别统计"

    def __unicode__(self):
        return "< GenderStatistic: %s >" % self.id


class TreatmentHistory(models.Model):

    during_time = models.IntegerField(u"距离疗程开始日期")     # 单位为周
    course      = models.IntegerField(u"连续疗程")
    interval    = models.IntegerField(u"实际服用间隔时")
    medicine    = models.ForeignKey("medicine.Medicine", verbose_name=u"药物", related_name="treatment_history", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"用药历史"

    def __unicode__(self):
        return "< TreatmentHistory: %s >" % self.id


class ResistanceHistory(models.Model):

    resistance_gene = models.CharField(u"耐药基因", max_length=100)         
    time            = models.DateTimeField(auto_now_add=True, auto_now=True, verbose_name = u"检查出耐药距离现在的时间")
    medicine        = models.ForeignKey("medicine.Medicine", verbose_name=u"药物", related_name="treats", null=True, blank=True)


    class Meta:
        verbose_name_plural = u"耐药历史"

    def __unicode__(self):
        return "< ResistanceHistory of %s >" % self.medicine.name


class BaseLineItem(models.Model):

    average             = models.FloatField(u"平均数值")
    statistical_confine = models.OneToOneField("indicator.StatisticalConfine", verbose_name=u"统计数值范围", related_name="base_line_items", null=True, blank=True)
    indicator           = models.ForeignKey("indicator.Indicator", verbose_name=u"医学指标", related_name="base_line_items", null=True, blank=True)
    sample              = models.ForeignKey("Sample", verbose_name=u"人群", related_name="base_line_items", null=True, blank=True)


    class Meta:
        verbose_name_plural = u"研究基线项目"

    def __unicode__(self):
        return "< BaseLineItem: %s >" % self.id
    

class Result(models.Model):

    indicator = models.ForeignKey("indicator.Indicator", verbose_name=u"医学指标", related_name="results", null=True, blank=True)

    #TODO: 结果可能是chart或followup_curve两者任选其一，需添加代码，验证至少提供了其中一个的数据
    chart             = models.OneToOneField("figure.Chart", verbose_name=u"柱状图", related_name="results", null=True, blank=True)
    followup_curve    = models.OneToOneField("figure.FollowupCurve", verbose_name=u"随访曲线", related_name="results", null=True, blank=True)
    

    class Meta:
        verbose_name_plural = u"实验结果"

    def __unicode__(self):
        return "< Result: %s >" % self.id

    def get_figure(self):
        return self.chart or self.followup_curve


admin.site.register([
                     Sample,
                     Age,
                     GenderStatistic,
                     TreatmentHistory,
                     ResistanceHistory,
                     BaseLineItem,
                     Result,
                    ])
