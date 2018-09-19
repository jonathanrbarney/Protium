from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from cis.models import Account
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class Account_Creation_Form(UserCreationForm):
    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Account

        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'middle_name', 'last_name', 'dob', 'phone_number', 'gender',
        'official_email', 'official_phone_number', 'profile_pic','discus_id', 'building', 'room_number')

class Account_Change_Form(UserChangeForm):
    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Account

        fields = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'dob', 'phone_number' , 'gender',
                  'official_email', 'official_phone_number', 'profile_pic','discus_id')

class BaseUserForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class AuthForm(BaseUserForm):
    remember = forms.BooleanField(initial=True, required=False)
    user = None

    def clean(self):
        cleaned_data = super(AuthForm, self).clean()
        self.user = authenticate(username=cleaned_data.get('username'),
                                 password=cleaned_data.get('password'))
        if self.user is None:
            raise ValidationError(
                'That login doesn\t match any we have.',
                params={'type': '1'},
            )
        return cleaned_data
