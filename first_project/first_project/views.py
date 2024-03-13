import random
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import Http404
from .forms import LoginForm, RegistrationForm

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def prices(request):
    return render(request, 'prices.html')

# def register(request):
#     return render(request, 'register.html')

class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    extra_context = {
        'title': 'Авторизация на сайте'
    }

class CustomLogoutView(LogoutView):    
    template_name = 'logout.html'
    extra_context = {
        'title': 'Выход пользователя'
    }

class CustomRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    extra_context = {
        'title': 'Регистрация на сайте'
    }
    
    def get_success_url(self) -> str:
        return reverse('login')
    
    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)

class UserProfileView(TemplateView):
    template_name = 'profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404('Пользователь не найден')
        context['user_profile'] = user
        context['user_posts'] = ''
        context['title'] = f'Профиль пользователя {user}'
        return context