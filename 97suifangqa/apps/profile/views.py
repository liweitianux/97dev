# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render


# profile home {{{
def profile_view(request, username):
    """
    show profile of given user
    """
    return HttpResponse('Hi, %s' % username)
# }}}

