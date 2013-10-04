# -*- coding: utf-8 -*-

from django import forms
from django.template import loader
from django.utils.http import int_to_base36
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from django.utils.translation import ugettext, ugettext_lazy as _

from sfaccount.tasks import send_mail

import re


# AccountForm {{{
class AccountForm(forms.Form):
    """
    form for signing up a new account
    """
    username = forms.RegexField(regex=r'^[A-Za-z0-9_-]+$',
            max_length=30, label=u"用户名",
            help_text=u"由字母、数字和下划线组成，长度6-30位",
            error_messages={'invalid': u"用户名仅能包含字母、数字和下划线"},
    )
    email = forms.EmailField(max_length=75, label=u"邮箱")
    password1 = forms.CharField(label=u"密码", max_length=30,
            help_text=u"密码长度6-30位",
            widget=forms.PasswordInput)
    password2 = forms.CharField(label=u"确认密码", max_length=30,
            widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        # check length
        if len(username) < 6:
            raise forms.ValidationError(u'用户名长度需大于6位')
        # check first letter
        p = re.compile('[a-zA-Z_]')
        if p.match(username[0]):
            pass
        else:
            raise forms.ValidationError(u'首字母必须是字母或下划线')
        # check if exists
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'用户名已经被占用')

    def clean_email(self):
        try:
            User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(u'邮箱地址已经被占用')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 6:
            raise forms.ValidationError(u'密码长度需大于6位')
        return password1

    def clean(self):
        cd = self.cleaned_data
        if 'password1' in cd and 'password2' in cd:
            if cd['password1'] != cd['password2']:
                raise forms.ValidationError(u'两次输入的密码不一致')
        #
        return cd
# }}}


# SFPasswordResetForm {{{
class SFPasswordResetForm(forms.Form):
    """
    to replace django's 'PasswordResetForm'
    to use djcelery's async send mail
    """
    error_messages = {
        'unknown': _("That e-mail address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': _("The user account associated with this e-mail "
                      "address cannot reset the password."),
    }
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.txt',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None,
             html_email_template_name=None):
        """
        Generates a one-use only link for resetting password
        and sends to the user.
        """
        # validate first
        if not self.is_valid():
            return self
        # validated: has 'self.cleaned_data'
        email = self.cleaned_data['email']
        users = User.objects.filter(email__iexact=email)
        if not len(users):
            raise forms.ValidationError(self.error_messages['unknown'])
        for user in users:
            # make sure that no email is sent to a user that actually
            # has a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            body_text = loader.render_to_string(email_template_name, c)
            # html email
            if html_email_template_name:
                body_html = loader.render_to_string(html_email_template_name, c)
            else:
                body_html = None
            # send mail
            to = user.email
            send_mail(to, subject, body_text, body_html)
# }}}


