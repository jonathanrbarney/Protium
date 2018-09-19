from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from cis.submodels.discus import *
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from dal import autocomplete


class create_board(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description',)

class create_post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('message', 'is_anonymous',)


class account_search(forms.Form):
    name = forms.CharField()


class bioForm(forms.ModelForm):
    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Account
        fields = ('first_name', 'middle_name', 'last_name','dob', 'gender','profile_pic')


class locationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('building', 'room_number',)


class contactForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('official_email', 'official_phone_number','email', 'phone_number')
