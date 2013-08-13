# -*- coding: utf8 -*-
from django.contrib import admin
from django import forms
from django.db import models
from .models import SciBlog, ResultContent, EndPoint
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

def get_blogs(endp):
    blog = endp.blogs.all()[0]
    return "<a href='/admin/sciblog/sciblog/%s'>%s<a>" % (blog.id, blog.title)

get_blogs.short_description = "SciBlog"
get_blogs.allow_tags = True

class EndPointAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', get_blogs)



admin.site.register(SciBlog, SciBlogAdmin)
admin.site.register(EndPoint, EndPointAdmin)
