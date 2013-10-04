# -*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail_multipart(host,
                        port,
                        username,
                        password,
                        mail_from,
                        mail_to,
                        subject,
                        content_text=None,
                        content_html=None,
                        display_from=None):
    # create message container
    # correct MIME type is 'multipart/alternative'
    msg = MIMEMultipart('alternative')
    # from & to
    msg['From'] = display_from or mail_from
    if isinstance(mail_to, (list, tuple)):
        msg['To'] = ', '.join(mail_to)
    else:
        msg['To'] = mail_to
    # subject
    msg['Subject'] = subject
    # body (utf-8 encode required)
    if isinstance(content_text, unicode):
        content_text = content_text.encode('utf-8')
    if isinstance(content_html, unicode):
        content_html = content_html.encode('utf-8')
    text_part = MIMEText(content_text, 'plain')
    html_part = MIMEText(content_html, 'html')
    msg.attach(text_part)
    msg.attach(html_part)
    # send
    s = smtplib.SMTP()
    s.connect(host, port)
    s.login(username, password)
    s.sendmail(mail_from, mail_to, msg.as_string())
    s.quit()

