from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('search', views.post_search, name='post_search'),
    path('about', views.about, name='about'),
    path('register', views.user_register, name='user_register'),
<<<<<<< HEAD
    path('login', views.user_login, name='user_login')
=======
    path("accounts/profile", views.ProfileView.as_view(), name="profile"),
    path("accounts/login", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("accounts/logout", auth_views.LogoutView.as_view(), name="logout")
>>>>>>> parent of 7fcb089 (Revert "Update urls.py")
]