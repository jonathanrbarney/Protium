from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from athletics.serializers import *
from athletics.models import *
from url_filter.integrations.drf import DjangoFilterBackend
from athletics.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

class AFTViewSet(viewsets.ModelViewSet):
    queryset = AFT.objects.all()
    serializer_class = AFTSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields= ['score', 'creator__usafa_id','cadet__usafa_id']
    ordering_fields=['score']
    ordering=['score']
    permission_classes = [IsAuthenticated&AthScore]

class PFTViewSet(viewsets.ModelViewSet):
    queryset = PFT.objects.all()
    serializer_class = PFTSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields= ['score', 'creator__usafa_id','cadet__usafa_id']
    ordering_fields=['score']
    ordering=['score']
    permission_classes = [IsAuthenticated&AthScore]

    #def create(self, rq, *args, **kwargs):
     #   super(PFTViewSet, self).create(rq, *args, **kwargs)