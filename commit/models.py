from django.db import models

# Create your models here.


# 报告表
class Report(models.Model):

    # tapd对应单号
    tapd_id = models.IntegerField("tapd单号")
    # 报告标题
    name = models.CharField("名称", max_length=300)
    # 状态
    status = models.BooleanField("状态")
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
    comments = models.CharField("Comments", max_length=1000)
    # 创建时间(自动获取当前时间)
    create_time = models.DateTimeField("新增时间", auto_now=True)

    def __str__(self):
        return self.name

