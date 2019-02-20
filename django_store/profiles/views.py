from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import View, FormMixin, TemplateResponseMixin
from django.contrib.auth.forms import UserCreationForm

from .models import User, Customer
from .forms import UserForm, UserAuthentication


class UserCreate(View, TemplateResponseMixin, FormMixin):
    model = User
    form_class = UserForm
    template_name = 'profiles\\user_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response({"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=raw_password)
            login(request, user)
            return redirect('admin')
        return self.render_to_response({"form": form})


class UserLogin(LoginView):
    form_class = UserAuthentication
    template_name = 'profiles\\user_login.html'


class UserLogout(LogoutView):
    template_name = 'profiles\\user_logout.html'