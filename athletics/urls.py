from django.urls import include, path
from rest_framework import routers
from athletics import views

router = routers.DefaultRouter()
router.register(r'pft', views.PFTViewSet)
router.register(r'aft', views.AFTViewSet)

urlpatterns = [
    path('', include(router.urls)),
]