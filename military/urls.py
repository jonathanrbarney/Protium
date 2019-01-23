from django.urls import include, path
from rest_framework import routers
from military import views

router = routers.DefaultRouter()
router.register(r'positions', views.PositionViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'samis', views.SAMIViewSet)
router.register(r'amis', views.AMIViewSet)
router.register(r'pais', views.PAIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]