# -*- coding: utf-8 -*-

"""
97suifang local settings
"""


## social accounts settings
SOCIALOAUTH_SITES = (
    ('weibo', 'socialoauth.sites.weibo.Weibo', '新浪微博', {
        'redirect_uri': 'http://www.97suifang.com/account/oauth/weibo',
        'client_id': 'weibo_app_id',
        'client_secret': 'weibo_app_secret',
        }
    ),
)

