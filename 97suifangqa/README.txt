## async send mail:
-> sfaccount/README.txt

## run redis & celery
$ redis-server
$ python manage.py celeryd worker -E
$ python manage.py celerycam        (for monitoring)

