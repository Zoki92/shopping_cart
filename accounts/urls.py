
from django.urls import path
from .views import my_profile

urlpatterns = [
    path('profile/', my_profile, name='my_profile'),
]
