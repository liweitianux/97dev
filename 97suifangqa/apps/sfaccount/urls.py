# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

from django.contrib.auth import views as auth_views


urlpatterns = patterns('sfaccount.views',
    url(r'^signup/$', 'signup_view', name='signup'),
    # send activation mail
    url(r'^activate/send_mail/$', 'send_activation_mail_view',
        name='send_activation_mail'),
    # activate account
    url(r'^activate/$', 'activate_view', name='activate'),
    url(r'^activate/key/(?P<activation_key>[0-9a-zA-Z]+)/$',
        'activate_view',
        name='activate_key'),
    url(r'^activate/done/$', 'activate_done_view',
        name='activate_done'),
    # go home
    url(r'^home/$', 'go_home_view', name='go_home'),
)

urlpatterns += patterns('',
    # login & logout
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'sfaccount/login.html'},
        name='login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'sfaccount/logout.html'},
        name='logout'),
    # change password
    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name': 'sfaccount/password_change.html'},
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'sfaccount/password_change_done.html'},
        name='password_change_done'),
    # reset password
    # use own 'password_reset_view' to able to send multipart mail
    # use own 'SFPasswordResetForm' to use 'djcelery' to send email
    url(r'^password/reset/$',
        'sfaccount.views.password_reset_view',
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'sfaccount/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'sfaccount/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'sfaccount/password_reset_complete.html'},
        name='password_reset_complete'),
)


USING_SOCIAL_LOGIN = getattr(settings, 'USING_SOCIAL_LOGIN', False)
if USING_SOCIAL_LOGIN:
    urlpatterns += patterns('sfaccount.views',
        url(r'^oauth/(?P<sitename>\w+)/$',
            'social_login_callback', name='social_login_callback'),
    )


# test view
urlpatterns += patterns('',
    ## test
    url(r'^test/$',
        direct_to_template,
        { 'template': 'sfaccount/logout.html' },
        name='sfaccount_test'),
)

