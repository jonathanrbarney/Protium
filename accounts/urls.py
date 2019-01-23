from django.urls import include, path
from rest_framework import routers
from accounts import views

router = routers.DefaultRouter()
router.register(r'', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]