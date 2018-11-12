#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 11:26
# @Author  : Weiqiang.long
# @Site    : 
# @File    : views_api.py
# @Software: PyCharm

import json

import time
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from commit.models import Report
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib import auth


def login(request):
    """
    用户登录接口
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"status":100, "message":"用户名或密码错误"})
        else:
            auth.login(request, user)
            # 将cookie数据存入浏览器
            # response.set_cookie('username', username, 3600)

            # 将 session 信息记录到浏览器
            request.session['user'] = username

            users = User.objects.filter(username=username)
            data = []
            for user in users:

                user_dict = {
                    "user_id": user.id,
                    "user_name": username
                }

                # 将字典添加到数组中
                data.append(user_dict)

            return JsonResponse({"status":200, "message":"登录成功", "data":data})
    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})


def get_report_list(request):
    """
    获取报告列表
    :param request:
    :return:
    """
    if request.method == "GET":

        # 查询所有发布会
        reports = Report.objects.all()

        report_list = []

        for report in reports:
            report_list.append(model_to_dict(report))

        print(report_list)

        data = {"status":200, "message":"请求成功", "data":report_list}

        return JsonResponse(data)
    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})


def add_report_list(requset):
    if requset.method == "POST":
        # # 获取前端以form表单方式传的参数
        # name = requset.POST.get("name", "")
        # limit = requset.POST.get("limit", "")
        # status = requset.POST.get("status", "")
        # address = requset.POST.get("address", "")
        # start_time = requset.POST.get("start_time", "")


        # 获取前端以json方式传的参数
        report_dict = json.loads(requset.body)

        tapd_id = report_dict["tapd_id"]
        name = report_dict["name"]
        status = report_dict["status"]
        release_time = report_dict["release_time"]
        environment = report_dict["environment"]
        tester = report_dict["tester"]
        developer = report_dict["developer"]
        project = report_dict["project"]
        comments = report_dict["comments"]
        is_plan = report_dict["is_plan"]
        create_user = report_dict["create_user"]

        create_user = User.objects.filter(username=create_user)
        get_user = None
        for user in create_user:
            get_user = user.id

        try:
            # 新增一条发布会信息
            Report.objects.create(tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                                  environment=environment, tester=tester, developer=developer, project=project,
                                  comments=comments, is_plan=is_plan, create_user=get_user)
        except ValidationError:
            # 对入参的时间格式进行校验，如格式有误，则抛出相应的错误
            error = "日期格式错误, 请参照:YYYY-MM-DD HH:MM:SS"
            return JsonResponse({"status":103, "message":error})

        # 如果所有校验均通过，则创建一条发布会，并返回
        return JsonResponse({"status":200, "message":"新增测试日报成功"})


    else:
        # 如果请求方式不是post，则抛出此信息
        return JsonResponse({"status":100, "message":"请求方式有误"})


def edit_report_list(requset):
    if requset.method == "POST":
        # # 获取前端以form表单方式传的参数
        # name = requset.POST.get("name", "")
        # limit = requset.POST.get("limit", "")
        # status = requset.POST.get("status", "")
        # address = requset.POST.get("address", "")
        # start_time = requset.POST.get("start_time", "")


        # 获取前端以json方式传的参数
        report_dict = json.loads(requset.body)

        id = report_dict["id"]
        tapd_id = report_dict["tapd_id"]
        name = report_dict["name"]
        status = report_dict["status"]
        release_time = report_dict["release_time"]
        environment = report_dict["environment"]
        tester = report_dict["tester"]
        developer = report_dict["developer"]
        project = report_dict["project"]
        comments = report_dict["comments"]
        is_plan = report_dict["is_plan"]

        try:
            # 新增一条发布会信息
            Report.objects.update(id=id, tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                                  environment=environment, tester=tester, developer=developer, project=project,
                                  comments=comments, is_plan=is_plan)
        except ValidationError:
            # 对入参的时间格式进行校验，如格式有误，则抛出相应的错误
            error = "日期格式错误, 请参照:YYYY-MM-DD HH:MM:SS"
            return JsonResponse({"status":103, "message":error})

        # 如果所有校验均通过，则创建一条发布会，并返回
        return JsonResponse({"status":200, "message":"更新测试日报成功"})


    else:
        # 如果请求方式不是post，则抛出此信息
        return JsonResponse({"status":100, "message":"请求方式有误"})


