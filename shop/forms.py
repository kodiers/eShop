__author__ = 'kodiers'
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shop.models import Basket, Goods
from django import forms

class MyUserCreationForm(UserCreationForm):
    """Custom form for user registration"""
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
