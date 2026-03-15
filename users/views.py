from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # отправка приветственного письма
        subject = 'Добро пожаловать!'
        message = f'Здравствуйте, {self.object.email}! Спасибо за регистрацию на нашем сайте.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.object.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        # автоматический вход после регистрации
        user = authenticate(self.request, username=self.object.email, password=form.cleaned_data['password1'])
        if user:
            login(self.request, user)
        return response

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('catalog:home')

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user