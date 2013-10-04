using 'django-celery' and 'redis' to implement the function
of 'async sending email' with the activation key for
newly registered user.

REF:
(1) use Celery in Django with a Redis backend
    http://killtheyak.com/django-celery-redis/
(2) django-siteuser

HOWTO run:
1) # pip install django-celery redis
2) for system, install package 'redis' (maybe 'redis-server')
3) add 'djcelery' to 'INSTALLED_APPS'
4) add settings for 'redis' & 'djcelery' in 'settings.py'
5) ajust 'SF_MAIL' settings in 'mail_settings.py'
6) $ redis-server
7) $ ./manage.py syncdb
8) $ ./manage.py celeryd worker -E
9) $ ./manage.py celerycam      (for monitoring)

TEST:
a) ./manage.py shell
   >>> from sfaccount.tasks import send_mail
   >>> send_mail(to, subject, body_text, body_html)

