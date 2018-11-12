from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from commit.models import Report
from commit.forms import AddReportForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


#当页面编辑新增删除后拿的全部数据，返回第一页的数据
def get_firstPage(dataModel):
    data_list = dataModel.objects.all()
    paginator = Paginator(data_list, NumberColumns)
    contacts = paginator.page(1)
    return contacts

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


# # 添加测试报告
# def add_report(request):
#     # 读取浏览器 session
#     user_session = request.session.get('user', '')
#
#     if request.method == 'POST':
#         form = AddReportForm(request.POST) # form 包含提交的数据
#         if form.is_valid():
#             tapd_id = form.cleaned_data['tapd_id']
#             name = form.cleaned_data['name']
#             status = form.cleaned_data['status']
#             release_time = form.cleaned_data['release_time']
#             environment = form.cleaned_data['environment']
#             tester = form.cleaned_data['tester']
#             developer = form.cleaned_data['developer']
#             project = form.cleaned_data['project']
#             comments = form.cleaned_data['comments']
#             is_plan = form.cleaned_data['is_plan']
#             if status is True:
#                 status = 1
#             else:
#                 status = 0
#
#             Report.objects.create(tapd_id=tapd_id,name=name,status=status,release_time=release_time,environment=environment,tester=tester
#                                   , developer=developer,project=project,comments=comments,is_plan=is_plan)
#             return render(request, "add_report.html", {"user": user_session, "form": form, "success": "新增测试报告成功!"})
#
#     else:
#         form = AddReportForm()
#
#     return render(request, "add_report.html", {"user": user_session, "form": form})


# 发送测试报告列表
def email_manage(request):
    # 将cookie数据从浏览器中取出
    # user_cookie = request.COOKIES.get('username', '')

    # 读取浏览器 session
    user_session = request.session.get('user', '')
    # 增加发布会查询
    report_list = Report.objects.all()
    print(report_list)

    return render(request, 'email.html', {'user':user_session, 'reports':report_list})


# def receive_data(request):
#     if request.POST:  # 如果数据提交
#         print('有提交')
#
#     select = request.POST.get('select', None)
#
#     text = request.POST.get('text', None)
#
#     time = request.POST.get('time', None)
#     print(select, text, time)
#     return render(request, "your_html.html", {"success": "新增测试报告成功!"})  # your_html.html改为你的html页面并且参考前面的博客建立url链接。



def add_report(request):
    if request.method == 'POST':
        # username = request.POST.get('username', '')
        # password = request.POST.get('password', '')

        tapd_id = request.POST.get('tapd_id', '')
        name = request.POST.get('story_name', '')
        status = request.POST.get('status', '')
        release_time = request.POST.get('release_time', '')
        environment = request.POST.get('environment', '')
        tester = request.POST.get('tester', '')
        developer = request.POST.get('developer', '')
        project = request.POST.get('project', '')
        comments = request.POST.get('comments', '')
        is_plan = request.POST.get('is_plan', '')
        print(tapd_id, name, status, release_time, environment, tester, developer, project, comments, is_plan)

        Report.objects.create(tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                              environment=environment, tester=tester
                              , developer=developer, project=project, comments=comments, is_plan=is_plan)
        return render(request, "add_test.html", {"success": "新增测试报告成功!"})
    else:
        return render(request, 'add_test.html')

# 新增测试报告1
def add_data(request):
    if request.method == 'POST':

        tapd_id = request.POST.get('tapd_id', '')
        name = request.POST.get('story_name', '')
        status = request.POST.get('status', '')
        release_time = request.POST.get('release_time', '')
        environment = request.POST.get('environment', '')
        tester = request.POST.get('tester', '')
        developer = request.POST.get('developer', '')
        project = request.POST.get('project', '')
        comments = request.POST.get('comments', '')
        is_plan = request.POST.get('is_plan', '')
        print(tapd_id, name, status, release_time, environment, tester, developer, project, comments, is_plan)

        Report.objects.create(tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                              environment=environment, tester=tester
                              , developer=developer, project=project, comments=comments, is_plan=is_plan)
        contacts=get_firstPage(Report)
        return render(request, "add_test1.html", {"reports": contacts})
    else:
        return render(request, 'add_test1.html')


# 编辑测试报告1
def edit_data(request):
    if request.method == 'POST':
        tapd_id = request.POST.get('tapd_id', '')
        name = request.POST.get('story_name', '')
        status = request.POST.get('status', '')
        release_time = request.POST.get('release_time', '')
        environment = request.POST.get('environment', '')
        tester = request.POST.get('tester', '')
        developer = request.POST.get('developer', '')
        project = request.POST.get('project', '')
        comments = request.POST.get('comments', '')
        is_plan = request.POST.get('is_plan', '')
        Report.objects.create(tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                              environment=environment, tester=tester
                              , developer=developer, project=project, comments=comments, is_plan=is_plan)
        contacts = get_firstPage(Report)
        return render(request, "add_test1.html", {"reports": contacts})
    else:
        return render(request, 'add_test1.html')



def sign_index(request, id):
    report = get_object_or_404(Report, id=id)
    report_list = Report.objects.filter(id=id)

    return render(request, "edit_test.html", {'reports':report})



def sign_index_action(request, id):
    report = get_object_or_404(Report, id=id)
    report_list = Report.objects.filter(id=id)


    tapd_id = request.POST.get('tapd_id', '')
    name = request.POST.get('story_name', '')
    status = request.POST.get('status', '')
    release_time = request.POST.get('release_time', '')
    environment = request.POST.get('environment', '')
    tester = request.POST.get('tester', '')
    developer = request.POST.get('developer', '')
    project = request.POST.get('project', '')
    comments = request.POST.get('comments', '')
    is_plan = request.POST.get('is_plan', '')

    Report.objects.filter(id=id).update(tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                                            environment=environment, tester=tester, developer=developer, project=project,
                                            comments=comments, is_plan=is_plan)
    return render(request, 'edit_test.html')




def edit_report(request):
    report_obj = Report.objects.filter(id=id).first()

    if request.method == "POST":
        tapd_id = request.POST.get('tapd_id', '')
        name = request.POST.get('story_name', '')
        status = request.POST.get('status', '')
        release_time = request.POST.get('release_time', '')
        environment = request.POST.get('environment', '')
        tester = request.POST.get('tester', '')
        developer = request.POST.get('developer', '')
        project = request.POST.get('project', '')
        comments = request.POST.get('comments', '')
        is_plan = request.POST.get('is_plan', '')

        Report.objects.filter(id=id).update(tapd_id=tapd_id, name=name, status=status, release_time=release_time,
                                            environment=environment, tester=tester, developer=developer, project=project,
                                            comments=comments, is_plan=is_plan)
        return render(request, "edit_test.html", {"report_obj": report_obj})
    else:
        return render(request, 'edit_test.html')








