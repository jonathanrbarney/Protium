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

class Day_Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)

class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)
    day_type = models.OneToOneField('Day_Type', on_delete=models.CASCADE)

class Period_Slot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    from_time = models.TimeField()
    to_time = models.TimeField()
    schedule=models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='slots')

class SCA_Restriction(models.Model):
    restriction = models.CharField(max_length=128)

class SCA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    number = models.IntegerField()
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    created_time = models.DateTimeField()
    approved_time = models.DateTimeField(blank=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'is_SCA': True}, related_name='%(class)s_approved')
    name = models.CharField(max_length=128, blank=False)
    summary = models.TextField(blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_created')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False)
    is_emergency = models.BooleanField(default=False)
    restrictions = models.ManyToManyField(SCA_Restriction, blank=True)

class FM18_Type(models.Model):
    type = models.CharField(max_length=128)

class Form_18(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    created_time = models.DateTimeField()
    name = models.CharField(max_length=128, blank=False)
    summary = models.TextField(blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_MDG': True},
                                related_name='%(class)s_created')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_Cadet': True},
                               related_name='%(class)s_member')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False)
    type = models.ManyToManyField(FM18_Type, blank=False)

class Day_Type_Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField()

class Admin_Excusal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_created')
    number = models.IntegerField()
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    created_time = models.DateTimeField()
    approved_time = models.DateTimeField(blank=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='%(class)s_aproved')
    reason = models.TextField(blank=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False, related_name='%(class)s_member')
    is_emergency = models.BooleanField(default=False)
    restrictions = models.CharField(max_length=300, blank=True)

    def approved_PP(self):
        return any([i.is_PP for i in self.approver])