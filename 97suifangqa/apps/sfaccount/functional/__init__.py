# -*- coding: utf-8 -*-

from django.conf import settings
from sfaccount.functional.mail import send_mail_multipart

EMAIL = settings.SF_EMAIL

def send_mail(to, subject, content_text=None, content_html=None):
    send_mail_multipart(
        host=EMAIL['smtp_host'],
        port=EMAIL['smtp_port'],
        username=EMAIL['username'],
        password=EMAIL['password'],
        mail_from=EMAIL['from'],
        mail_to=to,
        subject=subject,
        content_text=content_text,
        content_html=content_html,
        display_from=EMAIL['display_from']
    )

