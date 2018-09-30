from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *
import django.contrib.auth as auth
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget
from discus.models import *

class boardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description',)

class postForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('message','is_anonymous',)