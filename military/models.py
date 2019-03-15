from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.conf import settings
from django.urls import reverse
import random
from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
from datetime import date
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static


def get_all_subordinates(obj):
    r = []
    for i in obj.subordinates.all():
        r.append(i)
        _r = get_all_subordinates(i)
        r = r + _r
    return r


def get_all_supervisors(obj):
    r = []
    for i in obj.supervisors.all():
        r.append(i)
        _r = get_all_supervisors(i)
        r = r + _r
    return r

def get_all_account_subordinates(acct):
    r = []
    for i in acct.jobs.all():
        _r = get_all_subordinates(i)
        r = r + _r
    return r


def get_all_account_supervisors(acct):
    r = []
    for i in acct.supervisors.all():
        _r = get_all_supervisors(i)
        r = r + _r
    return r


# TODO: add unit/class intelligence to permission model
# that way you can only create/edit positions with class year at or below yours
# prevents a 4-dig from creating a position that the wing king holds.
# even if the positon is useless its about having that control.
# you know somebody would do something like that.
# also we don't want people to be able to randomly draft cadets from other units
# to have positions below them. still doesn't effect permissions but just annoying.

class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, blank=False)
    holder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs', blank=True,
                               null=True)
    supervisors = models.ManyToManyField('Position', blank=True, related_name='subordinates')
    is_cadet_job = models.BooleanField(default=True)

    @property
    def subordinate_ids(self):
        ids = []
        for i in self.subordinates.all():
            ids.append(i.id)
        return ids

    def __str__(self):
        return f'{self.unit} {self.name} ({self.holder})'


class AMI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cadet = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="amis")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)


class SAMI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cadet = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="aamis")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)


class PAI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cadet = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="pais")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, blank=False)
    positions = models.ManyToManyField(Position, related_name='units', blank=True)
    commanders = models.ManyToManyField(Position, related_name='units_commanded', blank=True)

    def __str__(self):
        return f'{self.name}'
