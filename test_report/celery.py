#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/14 16:48
# @Author  : Weiqiang.long
# @Site    : 
# @File    : celery.py
# @Software: PyCharm

from __future__ import absolute_import
import os
from celery import Celery, platforms

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_report.settings')

from django.conf import settings

app = Celery('Earth')
platforms.C_FORCE_ROOT = True

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))



