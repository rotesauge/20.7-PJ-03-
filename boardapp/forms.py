from django import forms
from .models import Post,Message
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from datetime import datetime

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['caption', 'text', 'сategory']


class MessageForm(forms.ModelForm):
   class Meta:
       model = Message
       fields = ['text']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class CodeForm(AuthenticationForm):
    code = forms.CharField(label='Код подтверждения')
