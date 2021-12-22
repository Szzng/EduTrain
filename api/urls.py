from django.urls import path
from . import apiviews

app_name = 'api'

urlpatterns = [
    path('course/', apiviews.CourseListAPI.as_view(), name='course'),
]
