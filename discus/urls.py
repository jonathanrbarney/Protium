from django.urls import include, path
from rest_framework import routers
from discus import views

router = routers.DefaultRouter()
router.register(r'board', views.BoardViewSet)
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]