from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
import django.contrib.auth as auth
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget

class departmentEdit(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name','summary', 'admins', 'instructors')
        widgets = {
            'admins': Select2MultipleWidget,
            'instructors': Select2MultipleWidget,
        }