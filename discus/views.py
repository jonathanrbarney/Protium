from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from discus.serializers import *
from discus.models import *


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer