#!/usr/bin/env python

import os
import sys

## GETTING-STARTED: make sure the next line points to your settings.py:
from cnto_warnings.utils import add_and_update_low_attendace_for_previous_month

os.environ['DJANGO_SETTINGS_MODULE'] = 'cnto.settings'
## GETTING-STARTED: make sure the next line points to your django project dir:
if 'OPENSHIFT_REPO_DIR' in os.environ:
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'cnto'))

    from distutils.sysconfig import get_python_lib
    os.environ['PYTHON_EGG_CACHE'] = get_python_lib()

import django


if __name__ == "__main__":

    print "Configuring Django..."
    django.setup()
    print "Django ready!"

    add_and_update_low_attendace_for_previous_month()
