from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from discus.serializers import *
from discus.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from discus.permissions import VotePermission


class BoardViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Board.objects.all().filter(is_archived=False)
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'description', 'name', ]
    ordering_fields = ['id', 'description', 'name', ]
    ordering=['name']

class PostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_classes = ['id','message']
    orderings_classes=['created']
    ordering=['created']

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated&VotePermission]
    filter_backends = [SearchFilter, OrderingFilter]