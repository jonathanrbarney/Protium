from accounts.serializers import *
from accounts.models import *
from rest_framework import viewsets, mixins
from accounts.permissions import *
from url_filter.integrations.drf import DjangoFilterBackend

class AccountViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsSelf]
    filter_backends = [DjangoFilterBackend]
    #filter_fields = ['username', 'email']