#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/14 16:48
# @Author  : Weiqiang.long
# @Site    : 
# @File    : celery.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_report.settings')

# 注册Celery的APP
app = Celery('test_report')

# 绑定配置文件
app.config_from_object('django.conf:settings')

# # Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# # 自动发现各个app下的tasks.py文件
# app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


