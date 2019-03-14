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
from academics.models import Program

class Account(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    bio = models.TextField(default ="Hi! I'm new here")
    usafa_id = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    usafa_id_backup = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    discus_id = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=25, blank=True)
    middle_name = models.CharField(max_length=25, blank=True)
    email_verified = models.BooleanField(blank=False, default=False)
    official_email_verified = models.BooleanField(blank=False, default=False)
    official_phone_verified = models.BooleanField(blank=False, default=False)
    phone_verified = models.BooleanField(blank=False, default=False)
    last_name = models.CharField(max_length=25, blank=True)
    hometown = models.CharField(max_length=200, blank=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=248, unique=True)
    official_email = models.EmailField(max_length=248, blank=True)
    official_phone_number = PhoneNumberField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    programs = models.ManyToManyField(Program, related_name='cadets')
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Attack Helicopter', 'Attack Helicopter'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        blank=True,
    )
    ACCOUNTS = (
        ('Applicant', 'Applicant'),
        ('Cadet', 'Cadet'),
        ('Instructor', 'Instructor'),
        ('Permanent Party', 'Permanent Party'),
        ('Coach', 'Coach'),
        ('Medical Staff', 'Medical Staff'),
        ('Facilities', 'Facilities'),
        ('Alumni', 'Alumni'),
        ('Other','Other'),
        ('None', 'None'),
    )

    account_type = models.CharField(max_length=30, choices=ACCOUNTS, default='None')
    has_attended = models.BooleanField(default=False)

    @property
    def age(self):
        born = self.dob
        today = datetime.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    room_number = models.CharField(max_length=7, blank=True)
    BUILDINGS = (
        ('Vandenberg Hall', 'Vandenberg Hall'),
        ('Sijan Hall', 'Sijan Hall'),
        ('Fairchild Hall', 'Fairchild Hall'),
        ('Harmon Hall', 'Harmon Hall'),
        ('Mitchell Hall', 'Mitchell Hall'),
        ('Arnold Hall', 'Arnold Hall'),
    )
    building = models.CharField(max_length=30, choices=BUILDINGS, blank=True)

    last_four = models.CharField(blank=True, max_length=4, validators=[MinLengthValidator(4)])
    SSN = models.CharField(max_length=128, blank=True)
    class_year = models.CharField(blank=True, max_length=4, validators=[MinLengthValidator(4)])
    academic_advisor = models.ForeignKey('Account', on_delete=models.SET_NULL, related_name='advisees', null=True,
                                         blank=True)

    @property
    def proper_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def generate_usafa_id(self):
        from random import randint
        gen_id = ''.join(["%s" % randint(0, 9) for num in range(0, 6)])
        while len(Account.objects.filter(usafa_id=gen_id)) > 0:
            gen_id = ''.join(["%s" % randint(0, 9) for num in range(0, 6)])
        self.usafa_id = gen_id
        self.usafa_id_backup = gen_id

    def save(self, *args, **kwargs):
        if self.usafa_id_backup == '':
            self.generate_usafa_id()
        super(Account, self).save(*args, **kwargs)

    def user_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(self.usafa_id, filename)

    profile_pic = models.ImageField(null=True, blank=True, upload_to=user_directory_path)

    def is_in(self, grp):
        return self.groups.filter(name=str(grp)).exists()

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} ({self.usafa_id})'
