"""Defines URL schemes for users."""

from django.urls import path, include
from  . import views

app_name = 'users'
urlpatterns = [
    # Enable URL authorization by default.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
]
