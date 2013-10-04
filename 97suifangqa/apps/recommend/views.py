# -*- coding: utf-8 -*-

"""
views for apps/recommend
"""

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404


# index
def recommend_index(request):
    """
    index view for apps/recommend
    """
    return HttpResponse("recommend index")

