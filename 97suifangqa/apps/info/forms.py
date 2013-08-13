# -*- coding: utf-8 -*-
from haystack.forms import SearchForm

from .models import Query
from .utils import split_word

class QuerySearchForm(SearchForm):
    u'''
    问题查询表单,主要完成两个工作：
        1. 指定查询的model为Query
        2. 重载clean_q，对查询语句进行分词
    '''

    def __init__(self,*args, **kwargs):
        u'''
        在__init__中指定查询的model为Query
        '''
        super(QuerySearchForm, self).__init__(*args, **kwargs)
        self.searchqueryset = self.searchqueryset.models(Query)
    
    def clean_q(self):
        q = self.cleaned_data['q']
        return split_word(q)
