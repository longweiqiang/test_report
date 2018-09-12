from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from commit.models import Report
from commit.forms import AddReportForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# 登录方法
def login(request):
    return render(request, 'login.html')


# 登录动作的处理
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
        else:
            auth.login(request, user)
            response = HttpResponseRedirect('/report_manage/')
            # 将cookie数据存入浏览器
            # response.set_cookie('username', username, 3600)

            # 将 session 信息记录到浏览器
            request.session['user'] = username
            return response
    else:
        return render(request, 'login.html')


# 测试组测试报告列表
@login_required
def report_manage(request):
    # 将cookie数据从浏览器中取出
    # user_cookie = request.COOKIES.get('username', '')

    # 读取浏览器 session
    user_session = request.session.get('user', '')
    # 增加发布会查询
    report_list = Report.objects.all()
    print(report_list)

    return render(request, 'report_manage.html', {'user':user_session, 'reports':report_list})


# 添加测试报告
def add_report(request):
    # 读取浏览器 session
    user_session = request.session.get('user', '')

    if request.method == 'POST':
        form = AddReportForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            tapd_id = form.cleaned_data['tapd_id']
            name = form.cleaned_data['name']
            status = form.cleaned_data['status']
            release_time = form.cleaned_data['release_time']
            environment = form.cleaned_data['environment']
            tester = form.cleaned_data['tester']
            developer = form.cleaned_data['developer']
            project = form.cleaned_data['project']
            comments = form.cleaned_data['comments']
            create_time = form.cleaned_data['create_time']
            if status is True:
                status = 1
            else:
                status = 0

            Event.objects.create(tapd_id=tapd_id,name=name,status=status,release_time=release_time,environment=environment,tester=tester,developer=developer,project=project,comments=comments,create_time=create_time)
            return render(request, "add_report.html", {"user": user_session, "form": form, "success": "新增测试报告成功!"})

    else:
        form = AddReportForm()

    return render(request, "add_report.html", {"user": user_session, "form": form})






