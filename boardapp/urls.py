"""
URL configuration for DjangoPostBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from .views import (PostV,
                    Posts,
                    Messages,
                    MessageV,
                    accept_message,
                    PostUpdate,
                    PostCreate,
                    PostDelete,
                    MessageCreate,
                    MessageUpdate,
                    MessageDelete,
                    login_view,
                    login_code_view)
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',                          Posts.as_view(),                         name='posts'),
    path('posts/<int:pk>',            PostV.as_view(),                         name='post'),
    path('posts/create/',             login_required(PostCreate.as_view()),    name='article_create'),
    path('posts/<int:pk>/update/',    login_required(PostUpdate.as_view()),    name='article_update'),
    path('posts/<int:pk>/delete/',    login_required(PostDelete.as_view()),    name='article_delete'),
    path('messages/',                 login_required(Messages.as_view()),      name='messages'),
    path('messages/<int:pk>',         login_required(MessageV.as_view()),      name='message'),
    path('messages/create/',          login_required(MessageCreate.as_view()), name='post_create'),
    path('messages/<int:pk>/update/', login_required(MessageUpdate.as_view()), name='post_update'),
    path('messages/<int:pk>/delete/', login_required(MessageDelete.as_view()), name='post_delete'),
    path('accept/',                   login_required(accept_message),          name='accept'),
    path('login/',                    login_view,                              name='login'),
    path('login_code/',               login_code_view,                         name='login_code'),
    path('logout/',                   LogoutView.as_view(template_name='sign/logout.html'),
                                      name='logout'),
    path('signup/',                   BaseRegisterView.as_view(template_name='sign/signup.html'),
                                      name='signup'),
              ]





