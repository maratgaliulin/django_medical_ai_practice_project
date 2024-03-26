"""
URL configuration for first_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from . import views, api
from django.conf.urls.static import static  
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),

    
    path('', views.IndexView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.CustomRegistrationView.as_view(), name='register'),
    path('prices/', views.PricesView.as_view(), name='prices'),


    path('<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('post/<slug:category_slug>/<slug:slug>', views.PostPageView.as_view(), name='post_page'),
    path('category/<slug:category_slug>/<slug:slug>/', views.CategoryPageView.as_view(), name='category_page'),

    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),

    path('<str:username>/settings/', views.UserSettingsView.as_view(), name='profile_settings'),  
    path('<str:username>/posts/', views.UserPostsView.as_view(), name='user_posts_page'),
]


# API паттерны
urlpatterns += [
    path('get-file/', api.GetFilePath.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)