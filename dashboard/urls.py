from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.main, name='dashboard_main'),
    path('creator/', views.creator_dashboard, name='dashboard_new'),
    path('inquiry/', views.index_form, name='inquiry'),
    path('home_page/', views.home_page, name='home_page'),
    # url(r'^$', views.home, name='home'),
    # url(r'^signup/$', views.signup, name='signup'),
    path('token' , views.token_send , name="token_send"),
    path('success' , views.success , name='success'),
    path('verify_email' , views.verify_email , name="verify_email"),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),


    
    path('profiles/', views.profiles, name='profiles'),
    path('socials/', views.socials, name='socials'),

    path('assigned_campaign/', views.assigned_campaigns, name='assigned_campaign'),
    path('campaign_details/<int:id>/', views.campaign_details, name='campaign_details'),
    path('campaign_requests/', views.campaign_requests, name='campaign_requests'),
    path('accept_campaign/<int:id>/', views.accept_campaign, name='accept_campaign'),
    path('accepted_campaigns/', views.accepted_campaigns, name='accepted_campaigns'),
    path('negotiate/<int:id>', views.budget_negotiation, name='negotiate'),
    path('show_deliverables/<int:id>', views.show_deliverables, name='show_deliverables'),
    path('content_creation/<int:id>', views.content_creation, name='content_creation'),
    path('settle/<int:id>', views.settle_amount, name='settle_amount'),
    path('deliverable_done/<int:id>', views.deliverable_done, name='deliverable_done'),


]