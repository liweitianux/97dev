using 'django-celery' and 'redis' to implement the function
of 'async sending email' with the activation key for
newly registered user.

REF:
(1) use Celery in Django with a Redis backend
    http://killtheyak.com/django-celery-redis/

HOWTO run:
1) pip install django-celery redis
2) OS install package 'redis' (maybe 'redis-server')
3) add 'djcelery' to 'INSTALLED_APPS'
4) add settings for 'redis' & 'djcelery' in 'settings.py'
   SF_MAIL
5) system: $ redis-server
6) ./manage.py syncdb
7) ./manage.py celeryd worker -E

TEST:
a) ./manage.py shell
   >>> from sfaccount.tasks import send_mail
   >>> send_mail(to, subject, body)

