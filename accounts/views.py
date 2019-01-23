from django.contrib.auth.models import User, Group
from accounts.serializers import *
from accounts.models import *
from rest_framework import viewsets, mixins

class AccountViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer