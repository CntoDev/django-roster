#!/usr/bin/env python

import os
import sys

## GETTING-STARTED: make sure the next line points to your settings.py:
import traceback
import pytz

from datetime import datetime
from django.utils import timezone
from cnto.views.scrape import update_attendance_for_current_event

os.environ['DJANGO_SETTINGS_MODULE'] = 'cnto.settings'

## GETTING-STARTED: make sure the next line points to your django project dir:
if 'OPENSHIFT_REPO_DIR' in os.environ:
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'libs'))
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'cnto'))

    from distutils.sysconfig import get_python_lib

    os.environ['PYTHON_EGG_CACHE'] = get_python_lib()

import django

if __name__ == "__main__":

    dt = datetime.now()
    if dt.minute % 5 == 0:
        current_dt = timezone.make_aware(dt,
                                         timezone.get_default_timezone())
        event_day = current_dt.weekday() == 1 or current_dt.weekday == 4
        event_hour = current_dt.hour >= 20

        if event_day and event_hour:
            django.setup()

            update_attendance_for_current_event()
