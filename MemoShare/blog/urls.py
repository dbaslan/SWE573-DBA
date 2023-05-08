from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('search', views.post_search, name='post_search'),
    path('about', views.about, name='about'),
    path('profile', views.user_profile, name='user_profile'),
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login')
]