from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# 报告表
class Report(models.Model):

    # tapd对应单号
    tapd_id = models.IntegerField("tapd单号")
    # 报告标题
    name = models.CharField("名称", max_length=300)
    # 状态
    status = models.BooleanField("状态", blank=True, default="")
    # 上线时间
    release_time = models.DateTimeField("上线时间")
    # 环境
    environment = models.CharField("环境", max_length=200)
    # 测试人员
    tester = models.CharField("测试人员", max_length=200)
    # 开发人员
    developer = models.CharField("开发人员", max_length=200)
    # Project
    project = models.CharField("Project", max_length=600)
    # Comments
    comments = models.CharField("Comments", max_length=1000, blank=True, default="")
    # BUG数
    bug_total = models.IntegerField("BUG数")
    # 是否为计划上线
    is_plan = models.BooleanField("是否为计划上线", blank=True)
    # 创建人
    create_user = models.IntegerField("创建人")
    # 创建时间(自动获取当前时间)
    # 设置为True时，会在model对象第一次被创建时，将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新
    create_time = models.DateTimeField("新增时间", auto_now_add=True)
    # 更新时间
    # 设置为true时，能够在保存该字段时，将其值设置为当前时间，并且每次修改model，都会自动更新
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name

