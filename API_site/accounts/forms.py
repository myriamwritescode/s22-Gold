"""
this module defines all custom forms use
"""
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  # for customizing the user creation form here
from django.contrib.auth.models import User  # this is Django default user model
from django import forms

# this where our models form will sit

from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class CreateUserForm(UserCreationForm):  # here were you can modify the default User table
    email = forms.EmailField(required=True)  # add a new field email

    # age = forms.IntegerField() # add a new field age
    class Meta:
        model = User  # referring to the user model
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2']  # fields = ["username", "email","age", "password1", "password2"]
