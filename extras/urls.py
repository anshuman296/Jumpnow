from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.tnc, name='terms-and-conditions'),
]