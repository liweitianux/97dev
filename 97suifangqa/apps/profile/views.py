# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings 
from django.shortcuts import render
from django.contrib.auth.views import login, logout
from django.contrib.auth import login as auth_login

from .forms import UserCreationForm



def signup(request):
    u'''
    用户注册
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(request.REQUEST.get('next'))
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html',
                  locals())

