from django.urls import path
from . import views


app_name = 'register'

urlpatterns = [
    path('', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.UserUpdateView.as_view(), name='update'),
]