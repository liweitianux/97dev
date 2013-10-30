# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.list_detail import object_detail
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import utc

from sciblog import models as sm
from sciblog.forms import SciBlogSearchForm, ProperNounSearchForm
from info.forms import QuerySearchForm

import datetime
import itertools
import json


def blog_detail(request, blogid, block):
    u'''
    /blog/1/
    一个简单的显式blog详细内容的view函数
    '''
    block = block or "source"
    template = 'sciblog/blog_detail_%s.html' % block
    blog = get_object_or_404(sm.SciBlog, id=blogid)

    blockid = block

    # 用户已经收藏？
    collected = request.user.is_authenticated() and blog.collected_by.filter(id=request.user.id)

    # 用户已经懂了？
    understood = request.user.is_authenticated() and blog.catched_by.filter(id=request.user.id)

    # 与该文章相关的段落注释和专业名词
    annotations = blog.annotations.all_json(user=request.user)
    return render(request, template, locals())


def blog_index(request):
    """
    Temporary handler for index page render
    You might want to rename/relocate this
    """
    return render(request,"sciblog/index.html",locals())

def generator_has_content(generator):
    '''
    Returns (has_content, generator) based on the input generator

    If generator has at least one item, has_content is True.
    Otherwise, has_content is False.

    generator will return all items in the input generator
    '''
    #Simplified logic using itertools
    checkgen, outputgen = itertools.tee(generator, 2)
    has_content = False
    for item in checkgen:
        has_content = True
        break
    return (has_content, outputgen)

def objects_of_sqs(sqs):
    u'''
    返回search squery set结果对应的model object
    '''
    return itertools.imap(lambda x: x.object, sqs)

def limit(resultSet, count = 10):
    return itertools.islice(resultSet, count)

def query(request):
    u'''
    Blog查询
    '''

    tab = 'list'
    search_history = request.session.get('search_history', '').split('&&&')

    if request.method == 'GET':
        form = SciBlogSearchForm(request.GET)
    elif request.method == 'POST':
        form = SciBlogSearchForm(request.POST)

    if form.is_valid() and form.cleaned_data['q']:
        q = form.cleaned_data['q']
        search_history = [s for s in search_history if s != q]
        search_history.insert(0, q)
        search_history = search_history[0:5] #只保存最新的五条搜索记录
        request.session['search_history'] = '&&&'.join(search_history)

        results = form.search()
        (has_blogs, blogs) = generator_has_content(limit(objects_of_sqs(results),20))
        questuinsqs = QuerySearchForm(request.GET).search()
        (has_relate_questions, questions) = generator_has_content(limit(objects_of_sqs(questuinsqs),8))
        ppnounsqs = ProperNounSearchForm(request.GET).search()
        (hasppnouns, ppnouns) = generator_has_content(limit(objects_of_sqs(ppnounsqs),5))
        return render(request, 'sciblog/blog_list.html', locals())
    else:
        (has_blogs, blogs) = generator_has_content(limit(sm.SciBlog.objects.all(),30))
        return render(request, 'sciblog/blog_list.html', locals())


@login_required
def blog_collection(request):
    blogs = request.user.blog_collection.all()
    tab   = 'collection'
    has_blogs = len(blogs) > 0
    ppnouns = request.user.annotation_collection.all()
    has_ppnouns = request.user.annotation_collection.count() > 0
    return render(request, 'sciblog/blog_list_collection.html', locals())


@login_required
def add_user_to_m2m(request, objid, m2m='collected_by', model=sm.SciBlog):
    u'''
    响应收藏按钮和'懂了'按钮的点击
    '''

    result = {"error":False, 'added':True}
    result['id'] = objid 
    result['model'] = model._meta.verbose_name_plural
    model_name = model.__name__
    user = request.user
    try:
        obj = model.objects.get(id=objid)
        model_m2m = getattr(obj, m2m)
        if not model_m2m.filter(id=user.id):
            # 还没有收藏或点击懂了
            model_m2m.add(user)
            result['added'] = True
            # utc time
            now_utc = datetime.datetime.utcnow().replace(tzinfo=utc)
            # UserCollection
            uc, created = sm.UserCollection.objects.get_or_create(user=user)
            if model_name == 'SciBlog':
                if m2m == 'collected_by':
                    uc.lastCollectBlogTime = now_utc
                elif m2m == 'catched_by':
                    uc.lastCatchBlogTime = now_utc
            elif model_name == 'BlogAnnotation':
                if m2m == 'collected_by':
                    uc.lastCollectAnnotationTime = now_utc
            # save
            uc.save()
        else:
            # 已经收藏或点击了懂了
            model_m2m.remove(user)
            result['added'] = False
        result['times'] = model_m2m.count()
    except:
        result['error'] = True
        result['added'] = False

    return HttpResponse(json.dumps(result),
            mimetype = 'application/json')

def show_result(request, resultid):
    result  = get_object_or_404(sm.ResultContent, id=resultid)
    blog = result.blog
    return render(request, 'sciblog/blog_detail_results-detail.html', locals())
