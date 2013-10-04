# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect

from django.contrib.auth.tokens import default_token_generator

from sfaccount.models import Account
from sfaccount.forms import AccountForm, SFPasswordResetForm

# email address shown in the sent mail
FROM_EMAIL = getattr(settings, 'SF_EMAIL').get('display_from')


# go_home {{{
def go_home_view(request):
    """
    go to home page (profile)
    """
    if request.user.is_authenticated():
        username = request.user.username
        return redirect(reverse('profile_home',
            kwargs={'username': username}))
    else:
        # not logged in
        return redirect(reverse('login'))
# }}}


# signup {{{
def signup_view(request):
    """
    用户注册
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = AccountForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_account = Account.objects.create_inactive_account(
                    username=cd['username'],
                    email=cd['email'],
                    password=cd['password1'],
                    send_email=True
            )
            return HttpResponseRedirect(reverse('activate'))
    else:
        form = AccountForm()

    data = {
        'form': form,
    }
    return render(request, 'sfaccount/signup.html', data)
# }}}


# activate {{{
def activate_view(request, activation_key=None):
    """
    activate account

    if activation_key=None, then render a page ask user
        to provide the activation key;
    otherwise, directly activate the account and redirect
    """
    if activation_key:
        account = Account.objects.activate(activation_key)
        if account:
            # activated
            home_url = '/profile/%s/' % account.user.username
            return HttpResponseRedirect(home_url)
        else:
            # activate failed
            data = {'activate_failed': True}
            return render(request, 'sfaccount/activate.html', data)
    else:
        # ask user for the 'activation_key'
        return render(request, 'sfaccount/activate.html')
# }}}


# password_reset_view {{{
# own password_reset_view: enable to send multipart email
@csrf_protect
def password_reset_view(request, is_admin_site=False,
            template_name='sfaccount/password_reset.html',
            email_template_name='sfaccount/password_reset_email.txt',
            subject_template_name='sfaccount/password_reset_subject.txt',
            password_reset_form=SFPasswordResetForm,
            token_generator=default_token_generator,
            post_reset_redirect=None,
            from_email=FROM_EMAIL,
            current_app=None,
            extra_context=None,
            html_email_template_name='sfaccount/password_reset_email.html'):
    """
    re-write view to replace django's one
    able to send multipart email by using
    own 'SFPasswordResetForm' and 'send_mail'
    """
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
# }}}


# social_login_callback {{{
def social_login_callback(request, sitename):
    return HttpResponse('%s' % sitename)
# }}}

