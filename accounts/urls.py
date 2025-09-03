# accounts/urls.py

from django.urls import path

from .views import RegisterView, UserDetailView  # <-- Add UserDetailView here

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", UserDetailView.as_view(), name="user-detail"),  # <-- Add this line
]
