from django.db import models
from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
from datetime import date
from cis.models import *
from django.conf import settings

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1000)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False, related_name='instructed_courses')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='courses_created')
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False, related_name='managed_courses')
    terms_offered = models.ManyToManyField(Term, blank=True, related_name='courses')
    department = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prerequisites = models.ManyToManyField('self', blank=True, related_name='prerequisite_for')
    coerequisites = models.ManyToManyField('self', blank=True, related_name='coerequisite_of')
    summary = models.TextField()
    academic_credit_hours = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    military_credit_hours = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    athletic_credit_hours = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    archived = models.BooleanField(default=False)
    @property
    def is_active(self):
        return any([i.is_active for i in self.terms])

class Course_Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    program_schedule = models.ForeignKey('Program_Schedule', on_delete=models.CASCADE)
    term_instance = models.ForeignKey('Term_Instance', on_delete=models.CASCADE, related_name='course_instances')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    number_grade = models.DecimalField(max_digits=6, decimal_places=4)
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
    letter_grade_current = models.CharField(max_length=2, choices=GRADE_CHOICES)
    letter_grade_final = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)

    def quality_points(self):
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
        return GRADE_CHOICES[self.letter_grade]


class Department(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    name=models.CharField(max_length=300)
    faculty = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='%(class)s_faculty')
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='%(class)s_instructor')


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


class Course_Requirement(models.Model):
    program = models.ForeignKey('Program', on_delete = models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=300)
    courses_satisfy = models.ManyToManyField(Course, related_name='requirements_satisfied')
    #allow users easy way to select all courses in a department


class Term_Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=300)
    courses = models.ManyToManyField(Course)
    term_sequence_number = models.IntegerField()


class Program_Schedule_Template(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=300)




