import datetime
from cis.models import *
from django.conf import settings
from django.db import models
from django.urls import reverse
import random
from vote.models import VoteModel

class Board(VoteModel,models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    creator = models.ForeignKey('Account', on_delete=models.SET_NULL, related_name='boards', null=True)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    is_archived = models.BooleanField(default=False)

    def archive(self):
        self.is_archived=True
        return self

    def unarchive(self):
        self.is_archived=False
        return self

    @property
    def get_url(self):
        return reverse('discus_board', kwargs={'id': str(self.id)})


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creator = models.ForeignKey('Account', on_delete=models.SET_NULL, related_name='posts', null=True)
    is_anonymous = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    is_archived = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    reply_to = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    COLORS = (
        ('#940f15', '#940f15'),
        ('#2e598f', '#2e598f'),
        ('#0c2141', '#0c2141'),
    )
    def color_picker():
        COLORS = (
            ('#940f15', '#940f15'),
            ('#2e598f', '#2e598f'),
            ('#0c2141', '#0c2141'),
        )
        return random.choice(random.choice(COLORS))
    color = models.CharField(max_length=7, default=color_picker, choices=COLORS)

    def get_url(self):
        return reverse('discus_post', kwargs={'id': str(self.id)})
