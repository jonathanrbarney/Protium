"""protium URL Configuration

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
]

from django.urls import include, path
from rest_framework import routers
from athletics import views

router = routers.DefaultRouter()
router.register(r'athletics/pft', views.PFTViewSet)
router.register(r'athletics/aft', views.AFTViewSet)

from discus import views

router.register(r'discus/board', views.BoardViewSet)
router.register(r'discus/post', views.PostViewSet)
router.register(r'discus/vote', views.VoteViewSet)

from military import views

router.register(r'military/position', views.PositionViewSet)
router.register(r'military/unit', views.UnitViewSet)
router.register(r'military/sami', views.SAMIViewSet)
router.register(r'military/ami', views.AMIViewSet)
router.register(r'military/pai', views.PAIViewSet)

from academics import views

router.register(r'academics/term', views.TermViewSet)
router.register(r'academics/course', views.CourseViewSet)
router.register(r'academics/period', views.PeriodViewSet)
router.register(r'academics/section', views.SectionViewSet)
router.register(r'academics/enrollment', views.EnrollmentViewSet)
router.register(r'academics/registration', views.RegistrationViewSet)
router.register(r'academics/completion', views.CompletionViewSet)
router.register(r'academics/department', views.DepartmentViewSet)
router.register(r'academics/program', views.ProgramViewSet)
router.register(r'academics/requirement', views.RequirementViewSet)

from accounts import views

router.register(r'account', views.AccountViewSet)
from django.views.generic.base import RedirectView

urlpatterns += [
    path('v1/', include(router.urls), name='api'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/v1/', permanent=True), name='home'),
    path('v1/', include('knox.urls')),
    ]