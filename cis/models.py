from django.db import models
from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
import datetime
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.urls import reverse

class Account(AbstractUser):
    usafa_id = models.CharField(max_length=6, primary_key=True, unique=True, validators=[MinLengthValidator(6)])
    usafa_id_backup = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    discus_id = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=25, blank=True)
    middle_name = models.CharField(max_length=25, blank=True)
    email_verified = models.BooleanField(blank=False, default=False)
    official_email_verified = models.BooleanField(blank=False, default=False)
    official_phone_verified = models.BooleanField(blank=False, default=False)
    phone_verified = models.BooleanField(blank=False, default=False)
    last_name = models.CharField(max_length=25, blank=True)
    dob = models.DateField(blank=True)
    email = models.EmailField(max_length=248, unique=True)
    official_email = models.EmailField(max_length=248, blank=True)
    official_phone_number = PhoneNumberField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    GENDER = (
    ('M','Male'),
    ('F','Female'),
    ('A', 'Attack Helicopter'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        blank = True,
    )

    def calculate_age(self):
        born=self.dob
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    room_number = models.CharField(max_length=5)
    BUILDINGS = (
        ('Vandenberg Hall', 'Vandenberg Hall'),
        ('Sijan Hall', 'Sijan Hall'),
        ('Fairchild Hall', 'Fairchild Hall'),
        ('Harmon Hall', 'Harmon Hall'),
        ('Mitchell Hall', 'Mitchell Hall'),
        ('Arnold Hall', 'Arnold Hall'),
    )
    building = models.CharField(max_length=30, choices=BUILDINGS)

    last_four = models.CharField(blank=True, max_length=4, validators=[MinLengthValidator(4)])
    SSN = models.CharField(max_length=128, blank=True)
    class_year = models.CharField(blank=True, max_length=4, validators=[MinLengthValidator(4)])
    academic_advisor = models.ForeignKey('Account', on_delete=models.SET_NULL, related_name='advisees', null=True, blank=True)
    
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

    profile_pic = models.ImageField(blank=True, null=True,upload_to=user_directory_path)

    def is_in(self, grp):
        return self.groups.filter(name=str(grp)).exists()

    @property
    def group_dict(self):
        GRPS={}
        for i in self.groups.all():
            GRPS[i.name]=True
        return GRPS

    class Meta:
        ordering = ['last_name','first_name','middle_name']

    def get_absolute_url(self):
        return reverse('user_page', args=[str(self.usafa_id)])


    def __str__(self):
        return f'{self.username} ({self.first_name} {self.middle_name} {self.last_name})'


class Term(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sequence_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=1000)


    # def calculate_GPA(self):

class Program_Schedule(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.OneToOneField('Account', on_delete=models.CASCADE, limit_choices_to={'is_Cadet': True}, null=True, blank=True)


class Term_Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    program_schedule = models.ForeignKey('Program_Schedule', on_delete=models.CASCADE, related_name='term_instances')
    term = models.ForeignKey('Term', on_delete=models.CASCADE)
    GPA_Final = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    MPA_Final = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    PEA_Final = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

from cis.submodels.discus import *
from cis.submodels.academics import *
from cis.submodels.military import *
from cis.submodels.athletics import *
from cis.submodels.schedule import *


#class Instructor(models.Model):
#    User = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
#    last_four = models.CharField(blank=False, max_length=4, validators=[MinLengthValidator(4)])
#    SSN = models.CharField(max_length=128)
#    class_year = models.CharField(blank=False, max_length=4, validators=[MinLengthValidator(4)])
#
#    DORMITORIES = (
#        ('Vandenberg Hall', 'Vandenberg Hall'),
#        ('Sijan Hall', 'Sijan Hall'),
#    )
#
#   room_number = models.CharField(max_length=5)