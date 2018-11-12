#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 11:32
# @Author  : Weiqiang.long
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from commit import views_api

urlpatterns = [
    path('login/', views_api.login),
    path('logout/', views_api.logout),
    path('get_report_list/', views_api.get_report_list),
    path('add_report_list/', views_api.add_report_list),
    path('edit_report_list/', views_api.edit_report_list),





]

