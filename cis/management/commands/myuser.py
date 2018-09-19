from django.core.management.base import BaseCommand
from cis.models import *


class Command(BaseCommand):

    def handle(self, **options):
        p=Account()
        p.first_name='Jonathan'
        p.middle_name='Robert'
        p.last_name='Barney'
        p.username='jonathanrbarney'
        p.email='jonathanrbarney@gmail.com'
        p.phone_number='+14804941776'
        import datetime
        from django.contrib.auth.hashers import make_password
        p.password=make_password('foodfood')
        p.dob=datetime.date(year=1998,month=10,day=8)
        p.gender='M'
        p.is_staff=True
        p.is_superuser=True
        p.save()
        from django.contrib.auth.models import User, Group
        group = Group(name="cadet")
        group.save()
        group = Group(name="instructor")
        group.save()
        group = Group(name="privilegedInstructor")
        group.save()
        group = Group(name="academicAdmin")
        group.save()
        group = Group(name="commander")
        group.save()
        group = Group(name="militaryStaff")
        group.save()
        group = Group(name="athleticStaff")
        group.save()
        group = Group(name="mitchellHall")
        group.save()
        group = Group(name="militaryAdmin")
        group.save()
        group = Group(name="discusAdmin")
        group.save()
        group = Group(name="medGroup")
        group.save()
