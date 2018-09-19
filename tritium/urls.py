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
from django.urls import *
from . import views
from cis.models import Account
from decorator_include import decorator_include
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf.urls.static import static
from django.conf import settings


def full_user_required(view_func):
    user_login_required = user_passes_test(lambda user: user.has_bio(), login_url='/update_bio_info')
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func


urlpatterns = [
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^logout/$', views.account_logout, name='account_logout'),
    re_path(r'^login/$', views.account_login, name='account_login'),
    path('signup/', views.signup, name='signup'),
]
urlpatterns += [
    path('', decorator_include(login_required,'cis.urls'))
]
