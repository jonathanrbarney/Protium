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
import accounts.views as views
from accounts.models import Account
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('nucleus/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls')),
    re_path(r'^select2/', include('django_select2.urls')),
    re_path(r'^api-auth/', include('rest_framework.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('', login_required()(views.home), name='home'),
    re_path(r'^v1/', include('v1.urls')),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register,name='register'),
    path('accounts/', include('accounts.urls')),
    path('academics/', include('academics.urls')),
    path('admissions/', include('admissions.urls')),
    path('athletics/', include('athletics.urls')),
    path('discus/', include('discus.urls')),
    path('military/', include('military.urls')),
    path('cas/', include('cas.urls')),
]
