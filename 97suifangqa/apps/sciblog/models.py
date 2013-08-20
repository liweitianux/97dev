# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from utils import get_abstract
from .managers import *


# Create your models here.


# SciBlog {{{
class SciBlog(models.Model):

    title              = models.CharField(u"标题", max_length=400)
    subhead            = models.CharField(u"副标题", max_length=400, blank=True)
    entitle            = models.CharField(u"英文标题", max_length=400, blank=True)
    journal            = models.CharField(u"期刊", max_length=400, blank= True)
    publish_date       = models.DateField(u"出版日期", blank=True, null=True)
    readed_count       = models.PositiveIntegerField(u"被阅读次数", default=0)
    understanded_count = models.PositiveIntegerField(u"懂按钮被按次数", default=0)
    confused_count     = models.PositiveIntegerField(u"不懂按钮被按次数", default=0)
    ifvalue            = models.FloatField(u"影响因子", default=1.0)
    authors            = models.CharField(u"作者", max_length=1000, default="default authors")
    method             = models.TextField(u"治疗手段", blank=True)
    aim                = models.TextField(u"目标", blank=True)
    abstract_result    = models.TextField(u"结果简述", blank=True)
    abstractAE         = models.TextField(u"abstractAE", blank=True)
    treatment_content  = models.TextField(u"treatmentContent", blank=True)
    safety             = models.TextField(u"安全性", blank=True)

    hospital           = models.ManyToManyField("location.Hospital", verbose_name=u"作者医院", related_name="sciblogs", null=True, blank=True)
    guidline           = models.OneToOneField("Guideline", verbose_name=u"临床策略", related_name="blog", null=True, blank=True)
    baseline           = models.ManyToManyField("BaseLine", verbose_name=u"研究基线", related_name="blog", null=True, blank=True)
    endpoint_content   = models.TextField(u"治疗终点文本", blank=True)
    endpoints          = models.ManyToManyField("EndPoint", verbose_name=u"治疗终点", related_name="blogs", null=True, blank=True)
    clinic_conditions  = models.ManyToManyField("ClinicCondition", verbose_name=u"临床条件", related_name="blogs", null=True, blank=True)
    detectionAssay     = models.TextField(u"检测方法", blank=True)
    collected_by       = models.ManyToManyField(User, verbose_name=u"收藏者", related_name="blog_collection", null=True, blank=True)
    catched_by         = models.ManyToManyField(User, verbose_name=u"懂了的", related_name="blogs_catched", null=True, blank=True)

    # 从原BlogBlock拷贝过来的fields
    conclusion         = models.TextField(u"本文结论", blank=True)
    konwledge_piece    = models.ManyToManyField("KnowledgePiece", verbose_name=u"知识条目", related_name="blogs", null=True, blank=True)
    sample             = models.ManyToManyField("subjects.Sample", verbose_name=u"人群", related_name="blogs", null=True, blank=True)
    source             = models.OneToOneField("Source", verbose_name=u"出处", related_name="blog", null=True, blank=True)
    references         = models.ManyToManyField("Reference", verbose_name=u"参考信息", related_name="blogs", null=True, blank=True)
    query              = models.ManyToManyField("info.Query", verbose_name=u"问题", related_name="blogs", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"文章"

    def __unicode__(self):
        return "< SciBlog: %s >" % self.title

    def show(self):
        """
        used in 'search/search.html'
        to show search result
        """
        return self.__unicode__()

    def level(self):
        u'''
        计算文章难度等级
        '''
        return 1        #TODO:添加实现代码

    def quality_value(self):
        u'''
        计算文章质量
        '''
        return 1.0     #TODO:添加实现代码

    def communication_author(self):
        u'''
        找出通讯作者放在blog list
        '''
        return self.authors.split(',')[0]
# }}}


# ResultContent {{{
class ResultContent(models.Model):
    u'''
    实验结果内容
    '''
    type_choices = ((1, "total"),
                    (2, "now"),
                    (3, "future"))
    
    type = models.IntegerField(u"类型", choices=type_choices, null=True, blank=True)
    shorttitle = models.CharField(u"简标题", max_length=36, blank=True)
    abstract = models.CharField(u"摘要", max_length=100, blank=True)
    content = models.TextField(u"内容", blank = True)
    card_content = models.TextField(u"卡片内容", blank=True)
    sample  = models.ManyToManyField("subjects.Sample", verbose_name=u"人群", related_name="results", null=True, blank=True)
    blog = models.ForeignKey("SciBlog", verbose_name=u"文章", related_name="results", null=True, blank=True)
    indicators = models.ManyToManyField("indicator.Indicator", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"实验结果"

    def __unicode__(self):
        return "<ResultContent: %s>" % get_abstract(self.content)

    def color(self):
        u'''
        根据type返回卡片颜色
        '''

        return ['grey', 'green', 'blue'][self.type - 1]
# }}}


# Source {{{
class Source(models.Model):
    u'''
        这篇文章原论文的来源
    '''

    ensrc = models.CharField(u"英文出处", max_length=400, blank= True)
    chsrc = models.CharField(u"中文出处", max_length=400, blank= True)
    link  = models.URLField(verify_exists=False, max_length=400, blank=True, verbose_name = u"外网链接")


    class Meta:
        verbose_name_plural = u"出处"

    def __unicode__(self):
        return "< Source: %s >" % self.id
# }}}


# Reference {{{
class Reference(models.Model):
    u'''
        参考消息：这篇文章其他相关论文等信息的来源
    '''

    description = models.TextField(u"描述", blank=True)
    link        = models.URLField(verify_exists=False, max_length=400, blank=True, verbose_name = u"链接")


    class Meta:
        verbose_name_plural = u"参考信息"

    def __unicode__(self):
        return "< Reference: %s >" % self.description
# }}}


# KnowledgePiece {{{
class KnowledgePiece(models.Model):
    u'''
        知识条目：知识条目很可能是问题的答案。
    '''

    type_choices = ((0, u"科普知识"),
                    (1, u"科学评论"),
                   )
    
    title = models.CharField(u"标题", max_length=100, blank= True)
    content = models.TextField(u"条目内容", blank=True)
    type    = models.IntegerField(u"种类", choices=type_choices)
    objects = KnowledgePieceManager()
    

    class Meta:
        verbose_name_plural = u"知识条目"

    def __unicode__(self):
        return "< KnowledgePiece: %s %s >" % (self.id, self.content if len(self.content) < 20 else self.content[0:20])
# }}}


# BlogAnnotation {{{
class BlogAnnotation(models.Model):
    u'''
        文章注释
    '''

    PARAGRAPH = 0
    PROPER_NOUN = 1
    ANNOTATION_TYPES = (
        (PARAGRAPH, u"段落注释"),
        (PROPER_NOUN, u"专有名词"),
    )

    type = models.IntegerField(u"注释类型", choices=ANNOTATION_TYPES)
    no   = models.IntegerField(u"编号", blank=True, null=True)
    brief_content = models.CharField(u"简短内容", max_length=400,
            blank=True)
    detail = models.TextField(u"详细内容", blank=True)
    blogs = models.ManyToManyField("SciBlog", verbose_name=u"文章",
            related_name="annotations", null=True, blank=True)
    keywords = models.ManyToManyField("info.KeyWord",
            verbose_name=u"关键词", related_name="annotations",
            null=True, blank=True)
    figures = models.ManyToManyField("figure.Figure",
            verbose_name=u"图片", related_name="annotations",
            null=True, blank=True)
    collected_by = models.ManyToManyField(User,
            verbose_name=u"收藏者", related_name="annotation_collection",
            null=True, blank=True)
    objects = AnnotationManager()

    class Meta:
        verbose_name_plural = u"文章注释"

    def __unicode__(self):
        return "<BlogAnnotation: %s>" % get_abstract(self.brief_content)

    def show(self):
        """
        used in 'search/search.html'
        to show search result
        """
        return self.__unicode__()

    def get_absolute_url(self):
        # TODO
        return ''

    def firstkeyword(self):
        u'''
        第一个关键词,注意对于专有名词，通常只有一个
        '''

        return self.keywords.all()[0].content 

    def firstparagraph(self):
        u'''
        bloglist页面二上内容的阶段，
        django里面的注释第一段的末尾都是一个空格
        '''
        return self.detail.split(' ')[0]

    def is_collected_by(self, user):
        u'''
        该注释是否已经被user收藏
        '''
        if user.is_authenticated() and user.annotation_collection.filter(id=self.id):
            return True
        else:
            return False
# }}}


# Guideline {{{
class Guideline(models.Model):
    u'''
       临床策略 
    '''

    content = models.TextField(u"内容", blank=True)
    figures = models.ManyToManyField("figure.Figure", verbose_name=u"图片", related_name="guidlines", null=True, blank=True)


    class Meta:
        verbose_name_plural = u"临床策略"

    def __unicode__(self):
        return "<Guideline: %s>" % get_abstract(self.content)
# }}}


# EndPoint {{{
class EndPoint(models.Model):
    u'''
        治疗终点
    '''

    type_choices = ((1, "primary"),
                    (2, "secondary"),)

    content = models.TextField(u"内容", blank=True)
    type = models.IntegerField(u"类型", choices=type_choices, blank=True)
    indicator = models.ForeignKey("indicator.Indicator", verbose_name=u"医学指标", related_name="endpoints", null=True, blank=True)
    objects = EndPointManager()

    class Meta:
        verbose_name_plural = u"治疗终点"

    def __unicode__(self):
        return "<EndPoint: %s>" % get_abstract(self.content)
# }}}


# ClinicCondition {{{
class ClinicCondition(models.Model):
    u'''
        临床条件
    '''

    type_choices = ((0, "允许"),
                    (1, "排除"),)

    content = models.TextField(u"内容", blank=True)
    type = models.IntegerField(u"类型", choices=type_choices, blank=True)
    indicator = models.ForeignKey("indicator.Indicator", verbose_name=u"医学指标", related_name="clinic_conditions", null=True, blank=True)
    objects = ClinicConditionManager()


    class Meta:
        verbose_name_plural = u"临床条件"

    def __unicode__(self):
        return "<ClinicCondition: %s>" % get_abstract(self.content)
# }}}


# BaseLine {{{
class BaseLine(models.Model):
    u'''
        基线水平
    '''

    content = models.TextField(u"内容", blank=True)
    figures = models.ManyToManyField("figure.Figure", verbose_name=u"图片", related_name="baselines", null=True, blank=True)
    base_line_items = models.ManyToManyField("subjects.BaseLineItem", verbose_name=u"研究基线项目", related_name="baselines", null=True, blank=True)


    class Meta:
        verbose_name_plural = u"基线水平"

    def __unicode__(self):
        return "<BaseLine: %s>" % get_abstract(self.content)
# }}}



admin.site.register([
                     Source,
                     Reference,
                     KnowledgePiece,
                     Guideline,
                     ClinicCondition,
                     BaseLine,
                     ResultContent,
                     BlogAnnotation,
                    ])
