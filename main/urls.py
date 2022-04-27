from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [

    path('', views.jumpnow_main, name=''),
    path('terms/',views.tnc,name="tnc"),
    path('privacy_notice/', views.privacy,name="privacy_policy"),

    path('', views.jumpnow_main, name='home'),
    path('red/', views.redirect_fun, name='red'),
    path('contact_us/',views.contactUs,name="contact"),
    path('about/',views.aboutJN,name="aboutJN")


]