from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.main, name='chat'),
    path('history/<str:room_id>/', views.history, name='history'),
    path('save-message/', views.save, name='save_message'),
    path('save-file/<str:room_name>/', views.file_save, name='save-file'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('<str:room_name>/', views.room, name='room'),
]