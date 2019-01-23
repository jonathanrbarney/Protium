from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from military.serializers import *
from military.models import *


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class AMIViewSet(viewsets.ModelViewSet):
    queryset = AMI.objects.all()
    serializer_class = AMISerializer


class SAMIViewSet(viewsets.ModelViewSet):
    queryset = SAMI.objects.all()
    serializer_class = SAMISerializer


class PAIViewSet(viewsets.ModelViewSet):
    queryset = PAI.objects.all()
    serializer_class = PAISerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

