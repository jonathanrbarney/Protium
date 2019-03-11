from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from athletics.serializers import *
from athletics.models import *
from url_filter.integrations.drf import DjangoFilterBackend
from athletics.permissions import *

class AFTViewSet(viewsets.ModelViewSet):
    queryset = AFT.objects.all()
    serializer_class = AFTSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['creator', 'user']
    permission_classes = [IsCoach|IsSelf]


class PFTViewSet(viewsets.ModelViewSet):
    queryset = PFT.objects.all()
    serializer_class = PFTSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['creator', 'user']
    permission_classes = [IsCoach|IsSelf]

    #def create(self, rq, *args, **kwargs):
     #   super(PFTViewSet, self).create(rq, *args, **kwargs)