#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/14 16:49
# @Author  : Weiqiang.long
# @Site    : 
# @File    : tasks.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def hello_world():
    with open("output.txt", "a") as f:
        f.write("hello world")
        f.write("\n")
