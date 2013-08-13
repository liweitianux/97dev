# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.

class Figure(models.Model):

    legend      = models.CharField(u"图例", max_length=100, null=True, blank= True)
    title       = models.CharField(u"标题", max_length=100, null=True, blank= True)
    ori_img     = models.ImageField(upload_to="upload/ori-imgs/",verbose_name = u"原始图片")
    revised_img = models.ImageField(upload_to="upload/revised-imgs/",verbose_name = u"修改图片")
    comment     = models.TextField(u"注释", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"图片"

    def __unicode__(self):
        return "< Figure: %s >" % self.id
    

class Chart(models.Model):
    u'''
        柱状图里的一个柱子
    '''

    value  = models.FloatField(u"数值")
    figure = models.ForeignKey("Figure", verbose_name=u"图片", related_name="charts", null=True, blank=True)
    sample = models.OneToOneField("subjects.Sample", verbose_name=u"人群", related_name="charts", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"柱子"

    def __unicode__(self):
        return "< Chart: %s >" % self.id
    

class FollowupCurve(models.Model):
    u'''
        随访曲线里的某一根曲线提取出来，对应某个人群
    '''

    x      = models.CharField(u"x轴标签", max_length=100, blank=True)
    y      = models.CharField(u"y轴标签", max_length=100, blank=True)
    z      = models.CharField(u"z轴标签", max_length=100, blank=True)

    sample = models.OneToOneField("subjects.Sample", verbose_name=u"人群", related_name="followup_curves", null=True, blank=True)
    figure = models.ForeignKey("Figure", verbose_name=u"图片", related_name="followup_curves", null=True, blank=True)


    class Meta:
        verbose_name_plural = u"随访曲线"

    def __unicode__(self):
        return "< FollowupCurve: %s >" % self.id
    

class ValuesOfXYZ(models.Model):
    u'''
        一根曲线上的各个值 
    '''

    x = models.FloatField(u"x值")
    y = models.FloatField(u"y值")
    z = models.FloatField(u"z值")

    followup_curve = models.ForeignKey("FollowupCurve", verbose_name=u"随访曲线", related_name="xyz_values", null=True, blank=True)


    class Meta:
        verbose_name_plural = u"曲线上各点"

    def __unicode__(self):
        return "< ValuesOfXYZ: (%s,%s,%s) >" % (self.x, self.y, self.z)


admin.site.register([
                     Figure,
                     Chart,
                     FollowupCurve,
                     ValuesOfXYZ,
                    ])
