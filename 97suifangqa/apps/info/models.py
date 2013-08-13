# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class KeyWord(models.Model):

    content           = models.CharField(u"内容", max_length=200)
    description       = models.TextField(u"描述", blank=True)
    categoryid        = models.IntegerField(u"分类编号", null=True, blank=True)        #TODO:弄清这里的详细意义
    standard_judge    = models.BooleanField(u"是否为标准关键词", default=False)
    created_at        = models.DateTimeField(auto_now_add=True, verbose_name = u"创建时间")
    user              = models.ForeignKey(User, verbose_name=u"用户", related_name="keywords", null=True, blank=True)

    content_type      = models.ForeignKey(ContentType, null=True, blank=True)                                #将KeyWord作为GFK
    object_id         = models.PositiveIntegerField(null=True, blank=True)
    content_object    = generic.GenericForeignKey("content_type", "object_id")


    class Meta:
        verbose_name_plural = u"关键词"

    def __unicode__(self):
        return "< KeyWord: %s >" % self.content


# Query {{{
class Query(models.Model):

    content        = models.CharField(u"内容", max_length=500)
    level          = models.PositiveIntegerField(u"级数",default=1)
    categoryid     = models.IntegerField(u"分类编号", null=True, blank=True, default=1)        #TODO:弄清这里的详细意义
    created_at     = models.DateTimeField(auto_now_add=True, verbose_name = u"创建时间")
    standard_judge = models.BooleanField(u"是否为标准问题", default=False)
    user           = models.ForeignKey(User, verbose_name=u"用户", related_name="querys")

    content_type   = models.ForeignKey(ContentType, null=True, blank=True)                                #将Query作为GFK
    object_id      = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey("content_type", "object_id")


    class Meta:
        verbose_name_plural = u"问题"

    def __unicode__(self):
        return "< Query: %s >" % self.content

    def show(self):
        """
        used in 'search/search.html'
        to show search result
        """
        return self.__unicode__()
# }}}


class WordWordRelation(models.Model):

    value = models.FloatField(u"关联度")
    word1 = models.ForeignKey("KeyWord", verbose_name=u"关键词1", related_name="relations_with_other_words_as_primary", null=True, blank=True)
    word2 = models.ForeignKey("KeyWord", verbose_name=u"关键词2", related_name="relations_with_other_words_as_deputy", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"关键词与关键词的关系"

    def __unicode__(self):
        return "< WordWordRelation: (%s, %s) >" % (self.word1.content, self.word2.content)


class QueryQueryRelation(models.Model):

    value  = models.FloatField(u"关联度")
    query1 = models.ForeignKey("Query", verbose_name=u"问题1", related_name="relations_with_other_querys_as_primary", null=True, blank=True)
    query2 = models.ForeignKey("Query", verbose_name=u"问题2", related_name="relations_with_other_querys_as_deputy", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"问题与问题的关系"

    def __unicode__(self):
        return "< QueryQueryRelation: (%s, %s) >" % (self.query1.content, self.query2.content)


class WordQueryRelation(models.Model):

    value  = models.FloatField(u"关联度")
    word   = models.ForeignKey("KeyWord", verbose_name=u"关键词", related_name="relations_with_querys", null=True, blank=True)
    query2 = models.ForeignKey("Query", verbose_name=u"问题", related_name="relations_with_words", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"关键词与问题的关系"

    def __unicode__(self):
        return "< WordQueryRelation: (%s, %s) >" % (self.word.content, self.query.content)
    

class BlogQueryRelation(models.Model):

    value = models.FloatField(u"关联度")
    blog  = models.ForeignKey("sciblog.SciBlog", verbose_name=u"文章", related_name="relations_with_querys", null=True, blank=True)
    query = models.ForeignKey("Query", verbose_name=u"问题", related_name="relations_with_blogs", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"文章与问题的关系"

    def __unicode__(self):
        return "< BlogRelation: (%s, %s) >" % (self.blog.title, self.query.content)


admin.site.register([
                     KeyWord,
                     Query,
                     WordWordRelation,
                     WordQueryRelation,
                     BlogQueryRelation,
                    ])
