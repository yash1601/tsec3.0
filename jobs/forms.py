from django import forms
from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['solved', 'jobs']