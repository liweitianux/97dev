# -*- coding: utf-8 -*-

from celery import task

from sfaccount.functional import send_mail as _send_mail

@task
def send_mail(to, subject, content_text, content_html):
    _send_mail(to, subject, content_text, content_html)

