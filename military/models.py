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


class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length = 128, blank=False)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    holder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    supervisor = models.ManyToManyField('self',blank=True, related_name='supervisee')
    is_cadet_job = models.BooleanField(default=True)

    def is_above(self, pos):
        return pos in  self.get_all_supervisees()

    def is_below(self, pos):
        return pos in  self.get_all_supervisors()

    def get_all_supervisors(self, include_self):
        r = []
        if include_self:
            r.append(self)
            for c in self.supervisor:
                _r = c.get_all_supervisors(include_self=True)
                if 0 < len(_r):
                    r.extend(_r)
        return r

    def get_all_supervisees(self, include_self):
        r = []
        if include_self:
            r.append(self)
            for c in self.supervisee:
                _r = c.get_all_supervisees(include_self=True)
                if 0 < len(_r):
                    r.extend(_r)
        return r

class AMI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    term_instance = models.ForeignKey('academics.Term_Instance', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class SAMI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    term_instance = models.ForeignKey('academics.Term_Instance', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class PAI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    term_instance = models.ForeignKey('academics.Term_Instance', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, blank=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='units_member', through='Membership')
    positions = models.ManyToManyField(Position, related_name='units')
    commanders = models.ManyToManyField(Position, related_name='units_commanded')

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ratee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)

class Rating_Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    term = models.ForeignKey('academics.Term_Instance', on_delete=models.CASCADE)
    Membership = models.ForeignKey('Membership', on_delete=models.CASCADE)
    ratings = models.ManyToManyField(Rating, related_name='rating_table')

class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)