from django.contrib import admin
from django.urls import path
from payments import views
 
urlpatterns = [
    path('pay/<int:id>', views.pay, name='pay'),
    path('paymenthandler/<int:id>', views.paymenthandler, name='paymenthandler'),
    #Payment paths
]