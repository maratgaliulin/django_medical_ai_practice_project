from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import PostModel, CategoryModel, PostFilesModel


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя'
            }
        )
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }
        )
    )

    remember_me = forms.BooleanField(
       widget=forms.CheckboxInput(
           attrs={'class': 'checkbox'}),
        required=False        
       )
    

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']

class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя'
            })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите email'
            }
        )
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,17}$', message="Введите номер телефона в следующем формате: '+99999999999'. Можно вводить до 17 цифр.")

    phone = forms.CharField( 
        validators=[phone_regex],
        max_length=17,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            })
    )

    password1 = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            })
    )

    password2 = forms.CharField(
        max_length=128,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class UserInfoForm(forms.ModelForm):  
    username = forms.CharField(  
        max_length=150,  
        label='Имя пользователя (username)',  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите имя пользователя'  
        })  
    )  
    email = forms.EmailField(  
        widget=forms.EmailInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите email'  
        })  
    )  
    first_name = forms.CharField(  
        max_length=150,  
        label='Имя',  
        required=False,  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите ваше имя'  
        })  
    )  
    last_name = forms.CharField(  
        max_length=150,  
        label='Фамилия',  
        required=False,  
        widget=forms.TextInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите вашу фамилию'  
        })  
    )  

    class Meta:  
        model = User  
        fields = ['username', 'email', 'first_name', 'last_name']

class UserPasswordForm(PasswordChangeForm):  
    old_password = forms.CharField(  
        max_length=128,  
        label='Старый пароль',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите старый пароль'  
        })  
    )  
    new_password1 = forms.CharField(  
        max_length=128,  
        label='Новый пароль',  
        help_text=password_validation.password_validators_help_text_html(),  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Введите новый пароль'  
        })  
    )  
    new_password2 = forms.CharField(  
        max_length=128,  
        label='Подтверждение нового пароля',  
        widget=forms.PasswordInput(attrs={  
            'class': 'form-control',  
            'placeholder': 'Повторите новый пароль'  
        })  
    )

class AddPostByAuthorForm(forms.ModelForm):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in self.fields:  
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autofocus': ''})  

        self.fields['short_body'].widget.attrs.update({'class': 'django_ckeditor_5'})  
        self.fields['full_body'].widget.attrs.update({'class': 'django_ckeditor_5'})  
        self.fields['category'].widget.attrs.update({'class': 'form-select'})  
        self.fields["short_body"].required = False  
        self.fields["full_body"].required = False  

    class Meta:  
        model = PostModel  
        fields = ('title', 'image', 'category', 'short_body', 'full_body', 'status', 'file')
        
class AddCategoryByAuthorForm(forms.ModelForm):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in self.fields:  
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autofocus': ''})  

        self.fields['description'].widget.attrs.update({'class': 'django_ckeditor_5'})  

    class Meta:  
        model = CategoryModel  
        fields = ('title', 'parent', 'description')

