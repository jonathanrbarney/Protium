from django.db import models
from accounts.models import *
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

class PFT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    term_instance = models.ForeignKey('academics.Term_Instance', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class AFT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    term_instance = models.ForeignKey('academics.Term_Instance', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)