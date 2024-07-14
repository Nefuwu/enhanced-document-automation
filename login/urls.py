from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
]
