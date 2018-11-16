#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/14 16:49
# @Author  : Weiqiang.long
# @Site    : 
# @File    : tasks.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from .send_email import mail



@shared_task
def report():
    # 调用发送邮件方法
    mail()
