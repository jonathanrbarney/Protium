from accounts.serializers import *
from accounts.models import *
from rest_framework import viewsets, mixins
from accounts.permissions import *
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

class AccountViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSnapshot
    permission_classes = [IsAuthenticated&AccountPermission]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['usafa_id','first_name','middle_name','last_name', 'official_email',
                     'gender','class_year','account_type']
    ordering_fields = ['usafa_id','first_name','middle_name','last_name', 'official_email',
                     'gender','class_year','account_type']
class CreationTicketViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = CreationTicket.objects.all()
    serializer_class = CTSerializer
    permission_classes = [IsAuthenticated&CreationTicketPermission]
