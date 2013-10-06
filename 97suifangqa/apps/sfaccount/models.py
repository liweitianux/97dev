# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from django.utils.timezone import utc
from django.template.loader import render_to_string

from sfaccount.tasks import send_mail

import re
import random
import datetime


# SHA1 Hash regex
SHA1 = re.compile('^[a-f0-9]{40}$')


class AccountManager(models.Manager):                           # {{{
    """
    custom manager for 'Account' model
    """
    def activate(self, activation_key):
        """
        validate an activation key and activate the corresponding
        'User' if valid.

        if the key is valid and not expired, return the 'Account'
        if the key is invalid or expired, return 'False'
        if the key is valid but the 'User' is already activated,
            return 'False'

        reset the key string to prevent reactivation of an account
        which has been deactivated by the admin
        """
        if SHA1.search(activation_key):
            try:
                account = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not account.activation_key_expired():
                user = account.user
                user.is_active = True
                user.save()
                account.activation_key = self.model.ACTIVATED
                account.save()
                return account
        return False

    def create_inactive_account(self, username, email, password,
            send_email=True):
        """
        create a new, *local*, inactive 'User',
        and generate an 'Account' and
        email the activation key. return the new 'User'

        the activation key is a SHA1 hash, generated from
        a combination of the 'username' and a random slat
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()
        # create corresponding 'Account'
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        activation_key = sha_constructor(salt+username).hexdigest()
        new_account = self.create(user=new_user, is_social=False,
                activation_key=activation_key)
        new_account.save()
        # send email
        if send_email:
            new_account.send_activation_email()
        return new_account

    def delete_expired_accounts(self):
        """
        Remove expired instances of 'Account's and their
        associated 'User's.
        """
        for account in self.all():
            if account.activation_key_expired():
                user = account.user
                if not user.is_active:
                    user.delete()
                    account.delete()
# }}}


class Account(models.Model):                                    # {{{
    """
    Account model for 97suifang
    """
    ACTIVATED = u'ALREADY_ACTIVATED'

    user = models.OneToOneField(User, related_name="account")
    # username -> user.username
    # date_joined -> user.date_joined
    screen_name = models.CharField(u"昵称", max_length=30,
            null=True, blank=True)
    avatar = models.ImageField(u"头像", upload_to="uploads/avatars/",
            null=True, blank=True)
    # if social account
    is_social = models.BooleanField(default=False)
    # activation (SHA1 hash)
    activation_key = models.CharField(u"激活密钥", max_length=40)

    objects = AccountManager()

    class Meta:
        verbose_name_plural = u"账户信息"

    def __unicode__(self):
        if self.is_social:
            type = u"social"
        else:
            type = u"local"
        if self.user.is_active:
            state = u"activated"
        else:
            state = u"nonactivated"
        #
        return u'< Account: %s, %s, %s >' % (self.user.username,
                type, state)

    def activation_key_expired(self): # {{{
        """
        determine whether the activation key has expired

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        """
        expiration_days = datetime.timedelta(
                days=settings.ACCOUNT_ACTIVATION_DAYS)
        now_utc = datetime.datetime.utcnow().replace(tzinfo=utc)
        return self.user.is_active or (
                self.user.date_joined + expiration_days <= now_utc)
    # }}}

    def get_activation_url(self):
        return reverse('activate_key',
                kwargs={'activation_key': self.activation_key})

    # send_activation_email {{{
    def send_activation_email(self,
            async=None,
            subject_template_name='sfaccount/activation_email_subject.txt',
            email_template_name='sfaccount/activation_email_body.txt',
            html_email_template_name='sfaccount/activation_email_body.html'):
        """
        send an activation email to the newly registered user
        """
        ctx_dict = {
            'username': self.user.username,
            'activation_key': self.activation_key,
            'activation_url': self.get_activation_url(),
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        }
        subject = render_to_string(subject_template_name, ctx_dict)
        subject = ''.join(subject.splitlines())
        body_text = render_to_string(email_template_name, ctx_dict)
        body_html = render_to_string(html_email_template_name, ctx_dict)
        to = self.user.email
        # send email
        if async is None:
            async_send_mail = getattr(settings, 'ASYNC_SEND_MAIL', False)
        else:
            async_send_mail = async
        if async_send_mail:
            send_mail.delay(to, subject, body_text, body_html)
        else:
            send_mail(to, subject, body_text, body_html)
    # }}}

    def delete_account(self):
        user = self.user
        user.delete()
        self.delete()
# }}}


admin.site.register([Account])

# vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=python: #
