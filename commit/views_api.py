#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 11:26
# @Author  : Weiqiang.long
# @Site    : 
# @File    : views_api.py
# @Software: PyCharm

import json

import datetime
from time import sleep

import xlwt
from apscheduler.scheduler import Scheduler
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from commit.models import Report, Back_Config
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib import auth
from commit import send_email

import os
import pandas as pd
import pymysql
import numpy as np
import xlrd

from test_report import settings


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
            request.session['sessionid'] = username
            print(request.session['sessionid'])

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


# 退出接口
def logout(request):
    auth.logout(request)
    return JsonResponse({"status": 200, "message": "退出成功"})



def get_report_list(request):
    """
    获取报告列表
    :param request:
    :return:
    """
    if request.method == "POST":
        # user_id = request.POST.get('user_id', '')

        # 读取浏览器 session
        user_session = request.session.get('user', '')
        print(user_session)

        user_id = None
        if user_session != None:
            users = User.objects.filter(username=user_session)
            for user in users:
                user_id = user.id

        tapd_type = request.POST.get('tapd_type', '')
        tapd_id = request.POST.get('tapd_id', '')
        create_user = request.POST.get('create_user', '')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        pageNum = request.POST.get('pageNum', '')
        numPerPage = request.POST.get('numPerPage', '')

        if start_time:
            start_time = start_time + ' 00:00:00'
            print(start_time)
            end_time = end_time + ' 23:59:59'
            print(end_time)

        if user_id != '' and pageNum != '' and numPerPage != '':

            # 定一个字典用于保存前端发送过来的查询条件
            search_dict = dict()
            # 如果有这个值 就写入到字典中去
            if tapd_type != '':
                search_dict['tapd_type'] = tapd_type
            if tapd_id != '':
                search_dict['tapd_id'] = tapd_id
            if create_user != '':
                search_dict['create_user'] = create_user
            if user_id != 'admin':
                search_dict['create_user'] = user_id
            # if user_session != None:
            #     search_dict['login_user'] = user_session

            if start_time == '' or end_time == '':
                # 多条件查询 关键点在这个位置传如的字典前面一定要加上两个星号
                reports = Report.objects.filter(**search_dict)
            else:
                reports = Report.objects.filter(**search_dict, create_time__gte=start_time, create_time__lte=end_time)

        else:
            return JsonResponse({"status": 101, "message": "参数缺失"})




        paginator = Paginator(reports, numPerPage)
        # page = request.GET.get('page')
        try:
            contacts = paginator.page(pageNum)
        except PageNotAnInteger:
            # 如果page不是整型，或为None，取第一页
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)


        report_list = []

        for report in contacts:
            # report_list.append(model_to_dict(report))
            status = report.status
            if status == True:
                status = 1
            elif status == False:
                status = 0

            is_plan = report.is_plan
            if is_plan == True:
                is_plan = 1
            elif is_plan == False:
                is_plan = 0

            report_dict = {
                "id": report.id,
                "tapd_type": report.tapd_type,
                "tapd_id": report.tapd_id,
                "name": report.name,
                "status": status,
                "release_time": report.release_time,
                "environment": report.environment,
                "tester": report.tester,
                "developer": report.developer,
                "project": report.project,
                "comments": report.comments,
                "bug_total": report.bug_total,
                "is_plan": is_plan,
                "create_time": report.create_time,
                "create_user": report.create_user,
                "update_time": report.update_time
            }

            # 将字典添加到数组中
            report_list.append(report_dict)
            # print(report_list)
        total = len(reports)

        data = {"status": 200, "message": "请求成功", "total": total, "login_user": user_session, "data": report_list}

        response = JsonResponse(data)
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        # response["Access-Control-Max-Age"] = "1000"
        # response["Access-Control-Allow-Headers"] = "*"

        return response

    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})


def add_report(requset):
    """
    新增日报接口
    :param requset:
    :return:
    """
    if requset.method == "POST":
        # 获取前端以form表单方式传的参数
        tapd_type = requset.POST.get("tapd_type", "")
        tapd_id = requset.POST.get("tapd_id", "")
        name = requset.POST.get("name", "")
        status = requset.POST.get("status", "")
        release_time = requset.POST.get("release_time", "")
        # print("上线时间为：",release_time)
        environment = requset.POST.get("environment", "")
        tester = requset.POST.get("tester", "")
        developer = requset.POST.get("developer", "")
        project = requset.POST.get("project", "")
        comments = requset.POST.get("comments", "")
        bug_total = requset.POST.get("bug_total", "")
        is_plan = requset.POST.get("is_plan", "")
        create_user1 = requset.POST.get("create_user", "")
        # 读取浏览器 session
        # user_session = requset.session.get('user', '')
        # print(user_session)


        # # 获取前端以json方式传的参数
        # report_dict = json.loads(requset.body)
        #
        # tapd_type = report_dict["tapd_type"]
        # tapd_id = report_dict["tapd_id"]
        # name = report_dict["name"]
        # status = report_dict["status"]
        # release_time = report_dict["release_time"]
        # environment = report_dict["environment"]
        # tester = report_dict["tester"]
        # developer = report_dict["developer"]
        # project = report_dict["project"]
        # comments = report_dict["comments"]
        # bug_total = report_dict["bug_total"]
        # is_plan = report_dict["is_plan"]
        # create_user = report_dict["create_user"]

        create_user = User.objects.filter(username=create_user1)
        get_user = None
        for user in create_user:
            get_user = user.id

        try:
            # 新增一条发布会信息
            Report.objects.create(tapd_type=tapd_type, tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                                  environment=environment, tester=tester, developer=developer, project=project,
                                  comments=comments, bug_total=bug_total, is_plan=is_plan, create_user=get_user)
        except ValidationError:
            # 对入参的时间格式进行校验，如格式有误，则抛出相应的错误
            error = "日期格式错误, 请参照:YYYY-MM-DD HH:MM:SS"
            return JsonResponse({"status":103, "message":error})

        # 如果所有校验均通过，则创建一条发布会，并返回
        return JsonResponse({"status":200, "login_user":create_user1, "message":"新增测试日报成功"})


    else:
        # 如果请求方式不是post，则抛出此信息
        return JsonResponse({"status":100, "message":"请求方式有误"})


def edit_report(requset):
    """
    编辑日报接口
    :param requset:
    :return:
    """
    if requset.method == "POST":

        # 获取前端以form表单方式传的参数
        report_id = requset.POST.get("id", "")
        tapd_type = requset.POST.get("tapd_type", "")
        tapd_id = requset.POST.get("tapd_id", "")
        name = requset.POST.get("name", "")
        status = requset.POST.get("status", "")
        release_time = requset.POST.get("release_time", "")
        environment = requset.POST.get("environment", "")
        tester = requset.POST.get("tester", "")
        developer = requset.POST.get("developer", "")
        project = requset.POST.get("project", "")
        comments = requset.POST.get("comments", "")
        bug_total = requset.POST.get("bug_total", "")
        is_plan = requset.POST.get("is_plan", "")
        create_user1 = requset.POST.get("create_user", "")
        # 读取浏览器 session
        # user_session = requset.session.get('user', '')
        # print(user_session)

        # # 获取前端以json方式传的参数
        # report_dict = json.loads(requset.body)
        #
        # report_id = report_dict["id"]
        # tapd_type = report_dict["tapd_type"]
        # tapd_id = report_dict["tapd_id"]
        # name = report_dict["name"]
        # status = report_dict["status"]
        # release_time = report_dict["release_time"]
        # environment = report_dict["environment"]
        # tester = report_dict["tester"]
        # developer = report_dict["developer"]
        # project = report_dict["project"]
        # comments = report_dict["comments"]
        # bug_total = report_dict["bug_total"]
        # is_plan = report_dict["is_plan"]
        # create_user = report_dict["create_user"]

        create_user = User.objects.filter(username=create_user1)
        get_user = None
        for user in create_user:
            get_user = user.id

        try:
            # 更新测试日报
            # Report.objects.filter(id=report_id).update(tapd_id=tapd_id, name=name, status=status, release_time=release_time,
            #                       environment=environment, tester=tester, developer=developer, project=project,
            #                       comments=comments, bug_total=bug_total, is_plan=is_plan, create_user=get_user)
            report = Report.objects.get(id=report_id)

            report.tapd_type = tapd_type
            report.tapd_id = tapd_id
            report.name = name
            report.status = status
            report.release_time = release_time
            report.environment = environment
            report.tester = tester
            report.developer = developer
            report.project = project
            report.comments = comments
            report.bug_total = bug_total
            report.is_plan = is_plan
            report.create_user = get_user
            # 使用save()方法才能使用更新时间
            report.save()

        except ValidationError:
            # 对入参的时间格式进行校验，如格式有误，则抛出相应的错误
            error = "日期格式错误, 请参照:YYYY-MM-DD HH:MM:SS"
            return JsonResponse({"status":103, "message":error})

        # 如果所有校验均通过，则创建一条发布会，并返回
        return JsonResponse({"status":200, "login_user":create_user1, "message":"更新测试日报成功"})


    else:
        # 如果请求方式不是post，则抛出此信息
        return JsonResponse({"status":100, "message":"请求方式有误"})

# @login_required
def get_today_report_list(request):
    """
    获取今日上线报告列表
    :param request:
    :return:
    """
    if request.method == "GET":

        # 获取当前时间
        now = datetime.datetime.now()


        # 获取今天零点
        zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                             microseconds=now.microsecond)
        # 获取23:59:59
        lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)

        # 通过今日时间查询所有发布会
        reports = Report.objects.filter(create_time__gte=zeroToday, create_time__lte=lastToday)


        report_list = []

        for report in reports:
            # report_list.append(model_to_dict(report))
            status = report.status
            if status == True:
                status = 1
            elif status == False:
                status = 0

            is_plan = report.is_plan
            if is_plan == True:
                is_plan = 1
            elif is_plan == False:
                is_plan = 0

            report_dict = {
                "id": report.id,
                "tapd_type": report.tapd_type,
                "tapd_id": report.tapd_id,
                "name": report.name,
                "status": status,
                "release_time": report.release_time,
                "environment": report.environment,
                "tester": report.tester,
                "developer": report.developer,
                "project": report.project,
                "comments": report.comments,
                "bug_total": report.bug_total,
                "is_plan": is_plan,
                "create_time": report.create_time,
                "create_user": report.create_user,
                "update_time": report.update_time
            }

            # 将字典添加到数组中
            report_list.append(report_dict)
            print(report_list)
        total = len(reports)

        data = {"status": 200, "message": "请求成功", "total": total, "data": report_list}

        response = JsonResponse(data)
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        # response["Access-Control-Max-Age"] = "1000"
        # response["Access-Control-Allow-Headers"] = "*"

        return response

    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})


def task_status(requset):
    """
    定时任务状态
    :param request:
    :return:
    """
    if requset.method == "POST":
        # 获取前端以form表单方式传的参数
        id = requset.POST.get("id", "")
        status = requset.POST.get("status", "")

        if id == '':
            task = Back_Config.objects.create(task_status=status)
            # 使用save()方法才能使用更新时间
            task.save()
        else:
            task = Back_Config.objects.get(id=1)
            task.task_status = status
            # 使用save()方法才能使用更新时间
            task.save()
        return JsonResponse({"status": 200, "message": "成功"})

    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})



def hand_send_email(requset):
    """
    手动发送邮件
    :param requset:
    :return:
    """
    if requset.method == "POST":
        id = requset.POST.get("id", "")

        task_status = Back_Config.objects.filter(id=1)
        for task in task_status:
            status = task.task_status
            # print(type(status))

            if status == 1:
                # email.mail()
                return JsonResponse({"status": 200, "message": "邮件发送成功"})
            else:
                return JsonResponse({"status": 101, "message": "请先关闭自动发送邮件功能"})

    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})



# def task_Fun():
#     '''
#     这里写定时任务
#     '''
#     sleep(1)
#
#
#
# sched = Scheduler()
#
#
# @sched.interval_schedule(seconds=6)
# def my_task1():
#     print('定时任务1开始\n')
#     task_Fun()
#     print('定时任务1结束\n')
#
# @sched.interval_schedule(hours=4)
# def my_task2():
#     print('定时任务2开始\n')
#     sleep(1)
#     print('定时任务2结束\n')
#
#
# sched.start()

def push_bug_list(request):
    """
    上传bug
    :param request:
    :return:
    """
    if request.method == "POST":
        content = request.FILES.get("upload", None)

        # 非空判断
        if not content:
            return JsonResponse({"status": 101, "message": "上传文件不能为空"})

        # 判断文件类型
        file = os.path.splitext(content.name)
        filename, type = file
        if type != '.xls':
            return JsonResponse({"status": 102, "message": "上传文件类型有误,只支持.xls类型"})

        file_dir = os.path.join(settings.MEDIIA_ROOT)
        filenames = str(content)
        for root, dirs, files in os.walk(file_dir):
            print("文件：", files)
            print("文件名：", filenames)

            if filenames in files:
                return JsonResponse({"status": 103, "message": "文件已存在,上传失败"})



        position = os.path.join(settings.MEDIIA_ROOT, content.name)

        # 获取上传文件的文件名，并将其存储到指定位置
        storage = open(position, 'wb+')  # 打开存储文件
        for chunk in content.chunks():  # 分块写入文件
            storage.write(chunk)
        storage.close()

        book = xlrd.open_workbook(position)
        sheet = book.sheet_by_index(0)
        # data = xlrd.open_workbook(content.name)
        # table = data.sheets()[0]
        # 将数据存入数据库
        db = pymysql.connect("localhost", "root", "123456", "test_report", use_unicode=True, charset="utf8")
        # print(table)
        # nrows = table.nrows #行数
        # ncols = table.ncols #列数
        # c1=arange(0,nrows,1)
        # print(c1)

        # start = 2  # 开始的行
        # end = 8  # 结束的行
        #
        # rows = end - start

        list_values = []
        for x in range(sheet.nrows):
            values = []
            row = sheet.row_values(x)
            for i in range(sheet.ncols):
                # print(value)
                values.append(row[i])
            list_values.append(values)
        # print(list_values)
        datamatrix = np.array(list_values)
        # print(datamatrix[1:])
        dict = datamatrix[1:]
        for i in dict:
            # print(i[1])
            bug_id = i[0]
            bug_name = i[1]
            priority = i[2]
            status = i[3]
            developer = i[4]
            tester = i[5]
            create_time = i[6]
            update_time = i[7]
            # print(update_time)

            sql = "insert into bug_data(bug_id, name, priority, status, developer, tester, create_time, update_time)"" \
            ""values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            bug_id, bug_name, priority, status, developer, tester, create_time, update_time)
            try:
                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = db.cursor()
                cursor.execute(sql)
            except Exception as e:
                # 发生错误时回滚
                db.rollback()
                print(str(e))
            else:
                db.commit()  # 事务提交
        print('事务处理成功')




        return JsonResponse({"status": 200, "message": "操作成功"})

    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})






