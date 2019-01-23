from django.urls import include, path
from rest_framework import routers
from academics import views

router = routers.DefaultRouter()
router.register(r'terms', views.TermViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'periods', views.PeriodViewSet)
router.register(r'sections', views.SectionViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'programs', views.ProgramViewSet)
router.register(r'requirements', views.RequirementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]