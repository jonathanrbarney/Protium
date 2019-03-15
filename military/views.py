from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from military.serializers import *
from military.models import *
from rest_framework.permissions import IsAuthenticated
from military.permissions import *
from rest_framework.filters import SearchFilter, OrderingFilter

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated&PositionPermission]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields= ['name', 'holder__id']
    ordering_fields=['name','unit__name']
    ordering=['name']


class AMIViewSet(viewsets.ModelViewSet):
    queryset = AMI.objects.all()
    serializer_class = AMISerializer
    permission_classes = [IsAuthenticated&MilScorePermission]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields= ['cadet__id',]
    ordering_fields=['cadet__id','score']
    ordering=['name']


class SAMIViewSet(viewsets.ModelViewSet):
    queryset = SAMI.objects.all()
    serializer_class = SAMISerializer
    permission_classes = [IsAuthenticated&MilScorePermission]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields= ['cadet__id',]
    ordering_fields=['cadet__id','score']
    ordering=['name']

class PAIViewSet(viewsets.ModelViewSet):
    queryset = PAI.objects.all()
    serializer_class = PAISerializer
    permission_classes = [IsAuthenticated&MilScorePermission]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields= ['cadet__id',]
    ordering_fields=['cadet__id','score']
    ordering=['name']

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

