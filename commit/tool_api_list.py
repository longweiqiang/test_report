#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 14:35
# @Author  : Weiqiang.long
# @Site    : 
# @File    : tool_api_list.py
# @Software: PyCharm

import hashlib
import json
import time

import oss2
from django.http import JsonResponse


def get_md5(request):
    """
    通过传入相关参数，进行md5加密，并返回32位加密后参数
    :param request:
    :return:
    """
    if request.method == "POST":
        channelId = request.POST.get('channelId', '')
        mobile = request.POST.get('mobile', '')
        secretKey = request.POST.get('secretKey', '')

        timestamp = request.POST.get('timestamp', '')
        # 当timestamp为空字符串时，就用当前时间
        if timestamp == '':
            timestamp = int(round(time.time() * 1000))
            print(timestamp)

        # 进行md5加密
        data = 'channelId={0}&mobile={1}&timestamp={2}'.format(channelId, mobile, timestamp)+secretKey
        print(data)
        md5_data = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
        print(md5_data)

        return JsonResponse({"status":200, "message":"加密成功", "data":{"md5_data":md5_data, "timestamp":str(timestamp)}})
    else:
        return JsonResponse({"status":100, "message":"请求方式有误"})


def get_oss_img(request):
    """
        生成签名URL
        :param path:文件名
        :param time:授权有效期,默认授权有效期为四天
        :return:签名URL
        """
    # MyAccessKeyId = 'LTAIyxkt6Uz6Lmob'
    # MyAccessKeySecret = 'GMr5YsbuwPyiluxnclDTbfBRyWXYGl'
    # MyEndpoint = 'oss-cn-hangzhou.aliyuncs.com'
    # MyBucketName = 'lwq573925242'

    MyAccessKeyId = 'LTAIGtLs9U0rENY6'
    MyAccessKeySecret = 'aXsG49CtClh3LRDlLMbdzReDx1gmrq'
    MyEndpoint = 'oss-cn-hangzhou.aliyuncs.com'
    MyBucketName = 'xjx-files'


    if request.method == "POST":
        path = request.POST.get('path', None)
        times = request.POST.get('times', None)
        # 为path缺失组装一个json
        path_error = {
            "code": 500,
            "msg": "path参数缺失！"
        }
        if path == None:
            return JsonResponse(path_error)

        elif times == None:
            times = 4
            # 换算time,用天数乘以86400秒(一天)
            time = times * 86400
            # print(times)
            auth = oss2.Auth(MyAccessKeyId, MyAccessKeySecret)
            bucket = oss2.Bucket(auth, MyEndpoint, MyBucketName)
            oss_url = bucket.sign_url('GET', path, time)
            code = '00'
            msg = u'请求成功'
            dict_data = {
                "code": code,
                "msg": msg,
                "url": oss_url
            }
            return JsonResponse(dict_data)

        else:
            # 转换times的数据类型为int
            times = int(times)
            # 换算time,用天数乘以86400秒(一天)
            time = times * 86400
            # print(times)
            auth = oss2.Auth(MyAccessKeyId, MyAccessKeySecret)
            bucket = oss2.Bucket(auth, MyEndpoint, MyBucketName)
            oss_url = bucket.sign_url('GET', path, time)
            code = '00'
            msg = u'请求成功'
            dict_data = {
                "code": code,
                "msg": msg,
                "url": oss_url
            }
            return JsonResponse(dict_data)

    if request.method == "GET":
        path = request.GET.get('path', None)
        times = request.GET.get('times', None)
        # 为path缺失组装一个json
        path_error = {
            "code": 500,
            "msg": "path参数缺失！"
        }
        if path == None:
            return JsonResponse(path_error)

        elif times == None:
            times = 4
            # 换算time,用天数乘以86400秒(一天)
            time = times * 86400
            # print(times)
            auth = oss2.Auth(MyAccessKeyId, MyAccessKeySecret)
            bucket = oss2.Bucket(auth, MyEndpoint, MyBucketName)
            oss_url = bucket.sign_url('GET', path, time)
            code = '00'
            msg = u'请求成功'
            dict_data = {
                "code": code,
                "msg": msg,
                "url": oss_url
            }
            return JsonResponse(dict_data)

        else:
            # 转换times的数据类型为int
            times = int(times)
            # 换算time,用天数乘以86400秒(一天)
            time = times * 86400
            # print(times)
            auth = oss2.Auth(MyAccessKeyId, MyAccessKeySecret)
            bucket = oss2.Bucket(auth, MyEndpoint, MyBucketName)
            oss_url = bucket.sign_url('GET', path, time)
            code = '00'
            msg = u'请求成功'
            dict_data = {
                "code": code,
                "msg": msg,
                "url": oss_url
            }
            return JsonResponse(dict_data)