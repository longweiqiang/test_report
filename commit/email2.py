#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 18:21
# @Author  : Weiqiang.long
# @Site    : 
# @File    : email2.py
# @Software: PyCharm
# TODO: 包含线上BUG的邮件

from email.utils import formataddr

import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_report.settings'
django.setup()

import smtplib
import pymysql
import time
import datetime
from email.mime.text import  MIMEText

my_sender = '573925242@qq.com'    # 发件人邮箱账号
my_pass = 'alllshsquiwibeei'              # 发件人邮箱密码(当时申请smtp给的口令)
my_user = 'longweiqiang@xianjinxia.com'      # 收件人邮箱账号，我这边发送给自己


def query_indb() :
    db = pymysql.conn = pymysql.connect(host = '127.0.0.1',
                       port = 3306,
                       user = 'root',
                       passwd = '123456',
                       db = 'test_report',
                       charset = 'utf8')
    cursor = db.cursor()

    # 获取当前时间
    now = datetime.datetime.now()
    # 昨天00:00:00
    yesterdayNow = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    zeroYesterday = yesterdayNow - datetime.timedelta(hours=yesterdayNow.hour, minutes=yesterdayNow.minute, seconds=yesterdayNow.second,microseconds=yesterdayNow.microsecond)
    # 昨天23:59:59
    lastYesterday = zeroYesterday + datetime.timedelta(hours=23, minutes=59, seconds=59)

    # 获取昨天的日期,格式:年-月-日
    yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y%m%d")  # 昨天日期
    # print(yesterday)

    # 查询线上bug
    bug_sql = "select * from commit_report where release_time >= '{0}' and release_time <= '{1}' and tapd_type = 1".format(
        str(zeroYesterday), str(lastYesterday))
    cursor.execute(bug_sql)
    bug_results = cursor.fetchall()

    # 非计划线上bug数量
    bug_sql_1 = "select * from commit_report where release_time >= '{0}' and release_time <= '{1}' and tapd_type = 1 and is_plan = 0".format(
        str(zeroYesterday), str(lastYesterday))
    cursor.execute(bug_sql_1)
    not_plan = cursor.fetchall()
    print(not_plan)
    print(str(not_plan))

    header = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head>'
    th = '<span style="color: rgb(80, 80, 79); font-family: 微软雅黑, sans-serif; font-size: 15px; line-height: normal; background-color: window;">Dear all,</span>'\
         '<p class="MsoNormal" style="margin-right: 0cm; margin-left: 0cm; font-size: 15px; font-family: 宋体; line-height: normal;"><span lang="EN-US" style="background-color: window;">' + str(yesterday) + '</span><span style="background-color: window;">测试报告</span>如下所示<span lang="EN-US">,</span>以下线上缺陷在<span style="white-space: nowrap;">预生产</span>测试通过：</p>'\
          '<p><strong>线上bug：<font color="#dd0000"><b>' + str(len(bug_results)) + '个(非计划' + str(
        len(not_plan)) + '个)' + '</font></strong></p>' \
                                '<table border="1" cellspacing="0" cellpadding="3" bordercolor="#000000" width="80%" align="center" >' \
                                '<tr bgcolor="#F79646">' \
                                '<th>ID</th>' \
                                '<th>summary</th>' \
                                '<th>status</th>' \
                                '<th>上线时间</th>' \
                                '<th>环境</th>' \
                                '<th>测试人员</th>' \
                                '<th>开发人员</th>' \
                                '<th>Project</th>' \
                                '<th>Comments</th>' \
                                '</tr>'
    tr = ''
    for row in bug_results:
        td = ''
        if row[1] is None:
            tapd_id = " "
        else:
            tapd_id = row[1]
        if row[2] is None:
            name = " "
        else:
            name = row[2]
        if row[3] is None:
            status = " "
        else:
            status = "pass"
        if row[4] is None:
            release_time = " "
        else:
            release_time = row[4]
            # print(release_time)
        if row[5] is None:
            environment = " "
        else:
            environment = row[5]
        if row[6] is None:
            tester = " "
        else:
            tester = row[6]
        if row[7] is None:
            developer = " "
        else:
            developer = row[7]
        if row[8] is None:
            project = " "
        else:
            project = row[8]
        if row[9] is None:
            comments = " "
        else:
            comments = row[9]
        if row[10] == 1:
            color = ""
        else:
            color = "red"

        td = td + '<td>' + '<font color=' + color + '>' + str(tapd_id) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(name) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(status) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(release_time) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(environment) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(tester) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(developer) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(project) + '</font>' + '</td>'
        td = td + '<td>' + '<font color=' + color + '>' + str(comments) + '</font>' + '</td>'
        tr = tr + '<tr>' + td + '</tr>'
    tr = tr
    body = tr
    tail='</table></body></html>'
    #将内容拼接成完整的HTML文档
    mail = header + th + body + tail
    db.close()
    return mail


def mail():
    ret = True
    try:
        mail_msg = query_indb()
        msg = MIMEText(mail_msg, 'html', 'utf-8')
        # msg=MIMEText('<邮件内容>','plain','utf-8')
        msg['From'] = formataddr(["xxxxx", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["xxxxx", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = '邮件主题'  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


if __name__ == '__main__' :
    print(query_indb())
    # (title,result) = query_indb()
    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    # if send_email(mail_to,str(yes_time.strftime('%Y-%m-%d')) + ' ' + title,result) == False :
    #     send_email_result("****@qq.com","Registered Users Count Email Send Failed","Registered Users Count Email Send Failed")

