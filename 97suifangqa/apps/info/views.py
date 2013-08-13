# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.template import RequestContext

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from .models import Query
from .forms import QuerySearchForm


def query(request):
    u'''
    问题查询
    '''
    if request.method == "GET":
        return render_to_response('search/query/index.html',
                        context_instance=RequestContext(request))

    else:
        form = QuerySearchForm(request.POST)
        results = form.search()
        q = request.POST.get('q', '')
        return render_to_response('search/query/index.html',
              locals()   
            , context_instance=RequestContext(request))
        
        
    

