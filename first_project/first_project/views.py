from django.db.models.base import Model as Model
from django.http.response import HttpResponseForbidden       
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from django.http import Http404
from .forms import LoginForm, RegistrationForm, UserInfoForm, UserPasswordForm
from .models import PostModel, CategoryModel

class CategoryPageView(ListView):
    model = PostModel
    template_name = 'category_page.html'
    context_object_name = 'category'

    def get_queryset(self):
        category = self.get_category()
        descendant_categories = category.get_descendants(include_self=True)
        return PostModel.objects.filter(category__in=descendant_categories)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context['category'] = category
        context['categories_list'] = CategoryModel.get_children(self=category)
        return context
    
    def get_category(self):
        if not hasattr(self, 'category'):
            self.category = CategoryModel.objects.get(slug=self.kwargs['slug'])
        return self.category

class PostPageView(DetailView):
    model = PostModel
    template_name = 'post_page.html'
    context_object_name = 'post'

    def get_object(self, queryset = None):
        obj = super().get_object(queryset=queryset)
        obj.save()
        return obj

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = CategoryModel.objects.all()
        context['latest_posts'] = PostModel.objects.alatest()
        return context

class AboutView(TemplateView):
    template_name = 'about.html'
    context_object_name = 'about'

    def get_object(self, queryset = None):
        obj = super().get_object(queryset=queryset)
        obj.save()
        return obj
    
class PricesView(TemplateView):
    template_name = 'prices.html'
    context_object_name = 'prices'

    def get_object(self, queryset = None):
        obj = super().get_object(queryset=queryset)
        obj.save()
        return obj

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
        context['user_posts'] = PostModel.objects.filter(author=user)[:5]
        context['title'] = f'Профиль пользователя {user}'
        return context
    
class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_settings.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("У вас нет доступа к этой странице.")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info_form'] = UserInfoForm(instance=self.request.user)
        context['user_password_form'] = UserPasswordForm(self.request.user)
        context['title'] = f'Настройки профиля {self.request.user}'
        return context
    
    def post(self, request, *args, **kwargs):
        if 'user_info_form' in request.POST:
            form = UserInfoForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Данные успешно изменены.')
                return redirect('profile_settings', form.cleaned_data.get('username'))
            else:
                context = self.get_context_data(*kwargs)
                context['user_info_form'] = form
                return render(request, self.template_name, context)
            
        elif 'user_password_form' in request.POST:
            form = UserPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пароль успешно изменен')
                return self.get(request, *args, **kwargs)
            else:
                context = self.get_context_data(**kwargs)
                context['user_password_form'] = form
                return render(request, self.template_name, context)
        else:
            return self.get(request, *args, **kwargs)
        
class UserPostsView(ListView):  
    template_name = 'user_posts_page.html'  
    context_object_name = 'posts'  

    def get_queryset(self):  
        return PostModel.objects.filter(author__username=self.kwargs.get('username'))  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        try:  
            author = get_object_or_404(User, username=self.kwargs.get("username"))  
        except User.DoesNotExist:  
            raise Http404("Пользователь не найден")  
        context['author'] = author  
        context['title'] = f'Посты пользователя {author}'  
        return context