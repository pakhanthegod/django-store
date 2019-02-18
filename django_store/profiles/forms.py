from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from .models import User, Customer


class UserForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'))
    first_name = forms.CharField(label=_('Имя'), max_length=40)
    last_name = forms.CharField(label=_('Фамилия'), max_length=40)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')