source ~/.bashrc
workon django-roster
cd ~/django-roster/wsgi/cnto
git pull --rebase
./manage.py collectstatic -c --noinput
systemctl restart uwsgi
