# -*- coding: utf-8 -*-
from haystack import indexes
import datetime
from .models import SciBlog, BlogAnnotation


class SciBlogIndex(indexes.SearchIndex, indexes.Indexable):
    u'''
    科学文章索引
    '''
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return SciBlog

    def index_queryset(self, using=None):
        u'''
        对所有文章进行索引
        '''
        return self.get_model().objects.all()

class ProperNounIndex(indexes.SearchIndex, indexes.Indexable):
    u'''
    专业名词索引
    '''
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return BlogAnnotation

    def index_queryset(self, using=None):
        u'''
        返回所有类型为专业名词类型的注释
        '''
        return self.get_model().objects.propernouns()
