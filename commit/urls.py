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
    path('add_report/', views_api.add_report),
    path('edit_report/', views_api.edit_report),
    path('get_today_report_list/', views_api.get_today_report_list),
    path('task_status/', views_api.task_status),
    path('hand_send_email/', views_api.hand_send_email),

]

