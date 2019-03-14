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
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="units")
    positions = models.ManyToManyField(Position, related_name='units')
    commanders = models.ManyToManyField(Position, related_name='units_commanded')