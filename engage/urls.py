from django.urls import path
from django.conf.urls import url, include

from engage import views

urlpatterns = [
    path('gigs/create/', views.create_gig, name='create-gig'),
    path('gigs/', views.gigs_main, name='gigs-main'),
    path('new-direct-offer/', views.create_direct_offer, name='create-direct-offer'),
    path('raise-dispute/', views.raise_dispute, name='raise-dispute'),
    path('create-gig-payment-link/<int:gig_id>/', views.create_gig_payment_object, name='create_gig_payment_object'),
    path('transfer-finished-amount/<int:gig_id>/', views.send_payment_to_influencer, name='send_payment_to_influencer'),
    path('gig-payment-done/', views.gig_payment_done, name='gig_payment_done'),
]
