#!/usr/bin/env bash
source ~/.bashrc
workon django-roster
cd ~/django-roster/wsgi/cnto
git pull --rebase
./manage.py collectstatic -c --noinput
./manage.py migrate
systemctl restart uwsgi
