## async send mail:
-> sfaccount/README.txt

## run redis & celery
$ redis-server
$ python manage.py celery worker --loglevel=info
$ python manage.py celerycam        # for monitoring

## 'redis' troubleshooting
如果 redis-server 启动时出现如下错误：
> [20101] 30 Oct 08:52:02 # Can't handle RDB format version 6
> 20101] 30 Oct 08:52:02 # Fatal error loading the DB. Exiting.
则尝试删除当前目录下的 'dump.rdb' 文件，然后重新启动。

