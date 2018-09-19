"""tritium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import *
from django.views.generic import RedirectView

urlpatterns = [
    re_path(r'^discus/$', views.discus_home, name='discus_home'),
    path('discus/board/<id>/', views.discus_board, name='discus_board'),
    path('discus/post/<id>/', views.discus_post, name='discus_post'),
    path('discus/new_board/', views.new_board, name='new_board'),
    path('discus/edit_board/<bid>/', views.edit_board, name='edit_board'),
    path('discus/board_archive/<uid>/', views.board_archive, name='board_archive'),
    path('discus/board_unarchive/<uid>/', views.board_unarchive, name='board_unarchive'),
    path('discus/new_post/<bid>/', views.new_post, name='new_post'),
    path('discus/delete_post/<bid>/<pid>/', views.delete_post, name='delete_post'),
    path('discus/new_reply/<pid>/', views.new_reply, name='new_reply'),
    path('discus/reply/<pid1>/<pid2>/', views.delete_reply, name='delete_reply'),
    path('discus/vote/<pid2>/', views.delete_reply, name='delete_reply'),
]

urlpatterns +=[
    path('user/<usafa_id>/', views.user_page, name='user_page'),
    path('', views.home, name='home'),
]

urlpatterns +=[
    path('directory/', views.directory.as_view(), name='directory'),
]
