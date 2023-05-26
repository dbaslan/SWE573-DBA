from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('post/<int:pk>/unlike/', views.post_unlike, name='post_unlike'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('search', views.post_search, name='post_search'),
    path('about', views.about, name='about'),
    path('user/<str:usernamex>/', views.user_page, name='user_page'),
    path('profile', views.user_profile, name='user_profile'),
    path('profile/edit', views.user_profile_edit, name='user_profile_edit'),
    path('profile/mail', views.user_mail_edit, name='user_mail_edit'),
    path('profile/password', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('user_profile'), template_name="blog/user_pw_edit.html")),
    path('profile/delete', views.user_delete, name='profile_delete'),
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)