# -*- coding: utf8 -*-
from django.contrib import admin
from django import forms
from django.db import models
from .models import SciBlog, ResultContent, EndPoint, BlogAnnotation

from utils.widget import MarkitUpWidget, TinyMceWidget

class ResultContentInline(admin.TabularInline):
    model = ResultContent


class SciBlogAdmin(admin.ModelAdmin):
    #formfield_overrides = {
    #    models.TextField: {'widget': TinyMceWidget},
    #}
    inlines = [
        ResultContentInline,
    ]
    filter_horizontal = ('hospital','konwledge_piece','endpoints','query')


def get_blogs(endp):
    blogList = endp.blogs.all()
    blogListWith3 = []
    for each in blogList:
        blogListWith3.append('#'+str(each.id))
    #blogsStringWith3 = "#".join(blogListWith3)
     
    #return "<a href='/admin/sciblog/sciblog/%s'>%s<a>" % (blog.id, blog.title)

    return blogListWith3

get_blogs.short_description = "SciBlog"
#get_blogs.allow_tags = True

class EndPointAdmin(admin.ModelAdmin):
    #list_display = ('__unicode__', get_blogs)
    list_display = ('__unicode__', 'type',get_blogs)
    search_fields = ['content']


class BlogAnnotationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','no')
    filter_horizontal = ('keywords',)



admin.site.register(SciBlog, SciBlogAdmin)
admin.site.register(EndPoint, EndPointAdmin)
admin.site.register(BlogAnnotation, BlogAnnotationAdmin)