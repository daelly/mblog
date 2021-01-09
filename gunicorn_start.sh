#!/bin/bash
NAME='mblog'
DJANGO_DIR=/alidata/server/django/mblog
SOCK_FILE=/alidata/server/django/mblog/gunicorn.sock
USER=root
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=mblog.settings
DJANGO_WSGI_MODULE=mblog.wsgi
LOG_DIR=/var/log/gunicorn

echo "starting $NAME as `whoami`"

cd $DJANGO_DIR
source ./venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

RUN_DIR=$(dirname $SOCK_FILE)
test -d $RUN_DIR || mkdir -p $RUN_DIR

exec ./venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
	--name $NAME \
	--workers $NUM_WORKERS \
	--user=$USER \
	--log-level=debug \
	--bind=unix:$SOCK_FILE \
	--access-logfile=${LOG_DIR}/gunicorn_access.log \
	--daemon
