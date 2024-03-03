from django.urls import path
from .views import djamal_admin

urlpatterns = [
    path('djamal/', djamal_admin, name='djamal_admin'),
]