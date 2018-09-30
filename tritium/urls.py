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
from decorator_include import decorator_include



urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^select2/', decorator_include(login_required, 'django_select2.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('', login_required()(views.home), name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register,name='register'),
    path('accounts/', include('accounts.urls')),
    path('academics/', decorator_include(login_required, 'academics.urls')),
    path('admissions/', decorator_include(login_required, 'admissions.urls')),
    path('athletics/', decorator_include(login_required, 'athletics.urls')),
    path('discus/', decorator_include(login_required, 'discus.urls')),
    path('military/', decorator_include(login_required, 'military.urls')),
    path('schedule/', decorator_include(login_required, 'schedule.urls')),
]
