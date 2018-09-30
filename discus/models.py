from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.conf import settings
from django.urls import reverse
import random
from vote.models import VoteModel
from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
from datetime import date
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Board(VoteModel,models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='boards', null=True)
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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='posts', null=True)
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
    color = models.CharField(max_length=7, default='', choices=COLORS)

    def color_picker(self):
        COLORS = (
            ('#940f15', '#940f15'),
            ('#2e598f', '#2e598f'),
            ('#0c2141', '#0c2141'),
        )
        return random.choice(random.choice(COLORS))

    def save(self, *args, **kwargs):
        if self.color == '':
            self.color=self.color_picker()
        super(Post, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('discus_post', kwargs={'id': str(self.id)})