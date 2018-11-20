"""test_report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from commit import views, views_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('report_list/', views.repost_list),

    # path('repost_list/', views.repost_list),
    path('repost_list/', views_api.get_report_list),
    path('login_action/', views.login_action),
    path('report_manage/', views.report_manage),
    path('email_manage/', views.email_manage),
    path('add_report/', views.add_report),
    # path('test/', views.receive_data),
    # path('add_test/', views.add_test),
    path('edit_test/', views.edit_report),
    path('sign_index/<int:id>/', views.sign_index),
    path('sign_index_action/<int:report_id>/', views.sign_index_action),
    # path('add_data/', views.add_data),
    # path('edit_data/', views.edit_data),
    path('upload/', views.upload),
    path('api/', include("commit.urls")),

]




