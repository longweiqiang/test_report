from django.contrib import admin
from commit.models import Report

# Register your models here.

# 把模型映射到admin后台
#增加发布会列表
class ReportAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ['id','tapd_id','name','status','release_time','environment','tester','developer','project','comments','create_time']
    # 搜索功能
    search_fields = ['tapa_id']
    # 过滤器
    list_filter = ['status']


admin.site.register(Report, ReportAdmin)