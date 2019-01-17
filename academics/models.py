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

class Term(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)
    from_date = models.DateField()
    to_date = models.DateField()
    @property
    def is_active(self):
        return self.from_date <= datetime.datetime.today() <= self.to_date
    def __str__(self):
        return f'{self.name}'

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)
    abbreviation = models.CharField(max_length=10)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False, related_name='instructed_courses')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='courses_created')
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False, related_name='managed_courses')
    terms = models.ManyToManyField(Term, blank=True, related_name='courses')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='courses')
    prerequisites = models.ManyToManyField('Course', blank=True, related_name='prerequisite_for')
    coerequisites = models.ManyToManyField('Course', blank=True, related_name='coerequisite_of')
    summary = models.TextField()
    academic_credit_hours = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=0)
    military_credit_hours = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=0)
    athletic_credit_hours = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=0)
    is_archived = models.BooleanField(default=False)
    public = models.BooleanField(default=True, blank=False)
    @property
    def is_active(self):
        return any([i.is_active for i in self.terms])
    def __str__(self):
        return f'{self.abbreviation} ({self.name})'

class Period(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)
    def __str__(self):
        return f'{self.name}'

class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sections_created')
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='%(class)s_instructed')
    term = models.ForeignKey(Term, on_delete = models.CASCADE, related_name='sections')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    max_students = models.IntegerField(null=True, blank=True)
    period = models.ManyToManyField(Period, related_name = 'sections')
    def __str__(self):
        return f'{self.period.all()[0]} {self.course.abbreviation}'

class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name="enrollments", null=True)
    number_grade = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    GRADE_CHOICES = (
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D', 'D'),
        ('F', 'Fail'),
        ('IC', 'Incomplete Controllable'),
        ('IU', 'Incomplete Uncontrollable'),
        ('W', 'Withdrawn'),
        ('WP', 'Withdrawn Passing'),
        ('WF', 'Withdrawn Failing'),
        ('P', 'Passing'),
        ('N', 'No Grade'),
    )
    letter_grade_current = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)
    letter_grade_final = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)

    def quality_points(self, grade):
        GRADE_CHOICES = {
            'A': 4.00,
            'A-': 3.70,
            'B+': 3.30,
            'B': 3.00,
            'B-': 2.70,
            'C+': 2.30,
            'C': 2.00,
            'C-': 1.70,
            'D': 1.00,
            'F': 0.00,
            'IC': None,
            'IU': None,
            'W': None,
            'WP': None,
            'WF': None,
            'P': None,
            'N': None,
        }
        return GRADE_CHOICES[grade]
    def __str__(self):
        return f'{self.student.last_name}, {self.student.first_name} ({self.student.usafa_id})'

class Department(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    name=models.CharField(max_length=300)
    abbreviation=models.CharField(max_length=10)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='%(class)s_faculty')
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='%(class)s_instructor')
    summary = models.TextField()
    is_archived = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name}'

class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    formal_name = models.CharField(max_length=300)
    informal_name = models.CharField(max_length=300)
    PROGRAM_TYPES = (
        ('Major','Major'),
        ('Minor','Minor'),
        ('Core','Core'),
        ('Scholars','Scholars'),
        ('Military', 'Military'),
        ('Athletic', 'Athletic'),
    )
    type = models.CharField(max_length=100, choices=PROGRAM_TYPES)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    cadets = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='programs')
    summary = models.TextField()
    credit_requirement = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f'{self.formal_name}'

class Course_Requirement(models.Model):
    program = models.ForeignKey('Program', on_delete = models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=300)
    courses_satisfy = models.ManyToManyField(Course, related_name='requirements_satisfied')
    def __str__(self):
        return f'{self.name}'

    #allow users easy way to select all courses in a department