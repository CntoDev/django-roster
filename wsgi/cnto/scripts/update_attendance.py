#!/usr/bin/env python

import os
import math
import sys

## GETTING-STARTED: make sure the next line points to your settings.py:

os.environ['DJANGO_SETTINGS_MODULE'] = 'cnto.settings'

## GETTING-STARTED: make sure the next line points to your django project dir:
if 'OPENSHIFT_REPO_DIR' in os.environ:
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'libs'))
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'cnto'))

    from distutils.sysconfig import get_python_lib

    os.environ['PYTHON_EGG_CACHE'] = get_python_lib()

import django
from datetime import datetime
from django.utils import timezone
from cnto.views.scrape import update_attendance_for_current_event

if __name__ == "__main__":

    dt = datetime.now()

    weekdays_to_monitor = [1, 4]
    event_start_hour = 20

    update_interval_seconds = 300
    update_interval_minutes = int(math.floor(update_interval_seconds / 60.0))

    if dt.minute % update_interval_minutes == 0:
        current_dt = timezone.make_aware(dt, timezone.get_default_timezone())
        event_day = current_dt.weekday() in weekdays_to_monitor
        event_hour = current_dt.hour >= event_start_hour

        if event_day and event_hour:
            django.setup()

            update_attendance_for_current_event(update_interval_seconds=update_interval_seconds,
                                                event_start_hour=event_start_hour,
                                                event_type_name="Unknown")
