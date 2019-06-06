#!/bin/bash

#命令只执行最后一个,所以用 &&

python3 manage.py collectstatic --noinput &&
python3 manage.py migrate &&
gunicorn weixin_test.wsgi:application -c gunicorn.conf
