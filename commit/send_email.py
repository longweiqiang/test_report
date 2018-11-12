#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/5 16:42
# @Author  : Weiqiang.long
# @Site    : 
# @File    : send_email.py
# @Software: PyCharm

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_report.settings'
django.setup()

from commit.models import Report


report_list = Report.objects.all()

my_sender = '573925242@qq.com'    # 发件人邮箱账号
my_pass = 'alllshsquiwibeei'              # 发件人邮箱密码(当时申请smtp给的口令)
my_user = 'longweiqiang@souyijie.com'      # 收件人邮箱账号，我这边发送给自己r

for report in report_list:
    tapd_id = report.tapd_id
    name = report.name
    status = report.status
    release_time = report.release_time
    environment = report.environment
    tester = report.tester
    developer = report.developer
    project = report.project
    comments = report.comments
    is_plan = report.is_plan

def mail():
    ret = True
    try:
        mail_msg = """<!DOCTYPE html>
<body>
<div id="container">
  <span style="color: rgb(80, 80, 79); font-family: 微软雅黑, sans-serif; font-size: 15px; line-height: normal; background-color: window;">Dear all,</span>
  <p class="MsoNormal" style="margin-right: 0cm; margin-left: 0cm; font-size: 15px; font-family: 宋体; line-height: normal;"><span lang="EN-US" style="background-color: window;">20181102</span><span style="background-color: window;">测试报告</span>如下所示<span lang="EN-US">,</span>以下需求在<span style="white-space: nowrap;">预生产</span>测试通过：</p>
  <p><strong>BUG数：0</strong></p>
  <div id="content">
<table border="0" cellpadding="0" cellspacing="0" width="1479" style="border-collapse:
 collapse;width:1110pt">

 <colgroup><col width="134" style="mso-width-source:userset;mso-width-alt:4288;width:101pt">
 <col width="291" style="mso-width-source:userset;mso-width-alt:9312;width:218pt">
 <col width="72" style="width:54pt">
 <col width="107" style="mso-width-source:userset;mso-width-alt:3424;width:80pt">
 <col width="125" style="mso-width-source:userset;mso-width-alt:4000;width:94pt">
 <col width="124" style="mso-width-source:userset;mso-width-alt:3968;width:93pt">
 <col width="211" style="mso-width-source:userset;mso-width-alt:6752;width:158pt">
 <col width="210" style="mso-width-source:userset;mso-width-alt:6720;width:158pt">
 <col width="205" style="mso-width-source:userset;mso-width-alt:6560;width:154pt">
 </colgroup><tbody><tr height="38" style="mso-height-source:userset;height:28.5pt">
  <td height="38" class="xl111" width="134" style="height: 28.5pt; width: 101pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: Tahoma, sans-serif; vertical-align: middle; border: 0.5pt solid windowtext; white-space: nowrap; background-color: rgb(141, 180, 227);">ID</td>
  <td class="xl111" width="291" style="border: 0.5pt solid windowtext; width: 218pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: Tahoma, sans-serif; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">summary</td>
  <td class="xl111" width="72" style="border: 0.5pt solid windowtext; width: 54pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: Tahoma, sans-serif; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">status</td>
  <td class="xl110" width="107" style="border: 0.5pt solid windowtext; width: 80pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: 宋体; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">上线时间</td>
  <td class="xl110" width="125" style="border: 0.5pt solid windowtext; width: 94pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: 宋体; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">环境</td>
  <td class="xl111" width="124" style="border: 0.5pt solid windowtext; width: 93pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: Tahoma, sans-serif; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">测试人员</td>
  <td class="xl110" width="211" style="border: 0.5pt solid windowtext; width: 158pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: 宋体; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">开发人员</td>
  <td class="xl111" width="210" style="border: 0.5pt solid windowtext; width: 158pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; font-size: 11pt; font-weight: 700; font-family: Tahoma, sans-serif; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">Project</td>
  <td class="xl112" width="205" style="border: 0.5pt solid windowtext; width: 154pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: windowtext; font-size: 11pt; font-weight: 700; font-family: Tahoma, sans-serif; vertical-align: middle; white-space: nowrap; background-color: rgb(141, 180, 227);">Comments</td>
 </tr>
 <tr height="122" style="mso-height-source:userset;height:91.5pt">
  <td height="122" class="xl114" align="right" style="height: 91.5pt; border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: rgb(54, 59, 66); font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;">{0}</td>
  <td class="xl114" style="border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: rgb(54, 59, 66); font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;">{1}</td>
  <td class="xl115" style="border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: rgb(54, 59, 66); font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;">{2}</td>
  <td class="xl116" style="border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: rgb(54, 59, 66); font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;"><span style="border-bottom:1px dashed #ccc;" t="5" times="">{3}</td>
  <td class="xl115" style="border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: rgb(54, 59, 66); font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;">{4}</td>
  <td class="xl115" style="border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: rgb(54, 59, 66); font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;">{5}</td>
  <td class="xl114" style="border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: rgb(54, 59, 66); font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;">{6}</td>
  <td class="xl117" width="210" style="border: 0.5pt solid windowtext; width: 158pt; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: windowtext; font-size: 11pt; font-family: 宋体; vertical-align: middle;">{7}</td>
  <td class="xl113" style="border: 0.5pt solid windowtext; padding-top: 1px; padding-right: 1px; padding-left: 1px; color: windowtext; font-size: 11pt; font-family: 宋体; vertical-align: middle; white-space: nowrap;">{8}</td>
 </tr>
 

</tbody></table>

""".format(tapd_id, name, status, release_time, environment, tester, developer, project, comments)
        msg=MIMEText(mail_msg, 'html', 'utf-8')
        # msg=MIMEText('<邮件内容>','plain','utf-8')
        msg['From']=formataddr(["xxxxx", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["xxxxx", my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']= '邮件主题'            # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user,], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

ret = mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")






