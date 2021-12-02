from django.urls import path
from . import views


app_name = 'course'

urlpatterns = [
    path('', views.CourseIndexView.as_view(), name='index'),
    path('test/', views.TestView.as_view(), name='test'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
    path('<str:pk>/', views.ByCategoryView.as_view(), name='bycategory'),
]