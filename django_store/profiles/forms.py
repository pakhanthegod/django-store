from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from .models import User, Customer


class UserForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        label=_('Имя'),
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        label=_('Фамилия'),
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserAuthentication(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )