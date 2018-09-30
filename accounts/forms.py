from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import *
import django.contrib.auth as auth
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget

class BaseUserForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class AuthForm(BaseUserForm):
    remember = forms.BooleanField(initial=True, required=False)
    user = None

    def clean(self):
        cleaned_data = super(AuthForm, self).clean()
        self.user = auth.authenticate(username=cleaned_data.get('username'),
                                      password=cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError("Wrong username or password.")
        elif not self.user.is_active:
            raise forms.ValidationError("The user is not activated.")
        return cleaned_data


class accountEdit(forms.ModelForm):
     class Meta:
        model = Account
        fields = ('__all__')