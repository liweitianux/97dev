# -*- coding: utf-8 -*-
from haystack.forms import SearchForm

from .models import SciBlog, BlogAnnotation

class SciBlogSearchForm(SearchForm):
    u'''
    问题查询表单,主要完成两个工作：
        1. 指定查询的model为Query
        2. 重载clean_q，对查询语句进行分词
    >>> from sciblog.forms import SciBlogSearchForm
    >>> form = SciBlogSearchForm({'q':u'干扰素'})
    >>> form.search()
        [<SearchResult: sciblog.sciblog (pk=u'1')>, <SearchResult: sciblog.sciblog (pk=u'3')>, <SearchResult: sciblog.sciblog (pk=u'2')>]
    '''

    def __init__(self,*args, **kwargs):
        u'''
        在__init__中指定查询的model为SciBlog
        '''
        super(SciBlogSearchForm, self).__init__(*args, **kwargs)
        self.searchqueryset = self.searchqueryset.models(SciBlog)


class ProperNounSearchForm(SearchForm):
    u'''
    专业名词搜索表单
    >>> from sciblog.forms import ProperNounSearchForm
    >>> form = ProperNounSearchForm({'q':u'乙肝'})
    >>> form.search()
        [<SearchResult: sciblog.blogannotation (pk=u'1')>]
    '''
    def __init__(self,*args, **kwargs):
        u'''
        在__init__中指定查询的model为BlogAnnotation
        '''
        super(ProperNounSearchForm, self).__init__(*args, **kwargs)
        self.searchqueryset = self.searchqueryset.models(BlogAnnotation)
