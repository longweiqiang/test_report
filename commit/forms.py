#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/12 17:05
# @Author  : Weiqiang.long
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from commit.models import Report
from django.contrib.admin import widgets

# 添加测试报告表单
class AddReportForm(forms.Form):

    # tapd对应单号
    tapd_id = forms.IntegerField()
    # 报告标题
    name = forms.CharField(max_length=300)
    # 状态
    status = forms.BooleanField(required=False)
    # 上线时间
    release_time = forms.DateTimeField(widget=widgets.AdminDateWidget())
    # 环境
    environment = forms.CharField(max_length=200)
    # 测试人员
    tester = forms.CharField(max_length=200)
    # 开发人员
    developer = forms.CharField(max_length=200)
    # Project
    project = forms.CharField(max_length=600)
    # Comments
    comments = forms.CharField(max_length=1000, required=False)
    # 是否为计划上线
    is_plan = forms.BooleanField(required=False)