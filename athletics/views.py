from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from athletics.serializers import *
from athletics.models import *


class AFTViewSet(viewsets.ModelViewSet):
    queryset = AFT.objects.all()
    serializer_class = AFTSerializer


class PFTViewSet(viewsets.ModelViewSet):
    queryset = PFT.objects.all()
    serializer_class = PFTSerializer