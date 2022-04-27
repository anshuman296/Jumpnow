from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.search, name='discovery_search'),
    # path('search/', views.search, name='discovery_search'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscriptions/basic/monthly/', views.discovery_subscription_montly, name='basic_subscription_monthly'),
    path('subscriptions/basic/yearly/', views.discovery_subscription_yearly, name='basic_subscription_yearly'),
    path('subscriptions/basic/done/monthly/', views.subscription_done_basic_monthly, name='sub-done-monthly'),
    path('subscriptions/basic/done/yearly/', views.subscription_done_basic_yearly, name='sub-done-yearly'),
    path('influencer/<int:pk>/', views.discoveryInfluencerProfile, name='influencer-profile'),
    path('campaigns/', views.discoveryCampaignsMain, name="discovery-camp-main"),
    path('campaigns/<int:pk>/', views.discoveryCampaignSingle, name="discovery-camp-single"),
    path('campaigns/list/<int:pk>/', views.campaignListSingle, name='single-list-cp'),
    path('api/export-influencer-list/', views.exportInfluencerList, name='export-inf-list'),
    path('api/get-campaigns/', views.getCampaigns, name='get-camp'),
    path('api/get-campaigns-list/<int:id>/', views.getCampaignLists, name='get-camp-list'),
    path('api/create-campaign-list/', views.addToCampaignLists, name='add-to-campaign-list'),
    path('marketer/profile/', views.marketerProfile, name='marketer-profile'),
    path('creator/profile/<int:id>/', views.CreatorDiscoveryProfile, name='creator-discovery-profile'),

    path('addcampaign/', views.Addcampaign, name='addcampaign'),
    path('addcampaignlist/', views.Addcampaignlist, name='addcampaignlist'),
    path('showcampaign/', views.showcampaigns, name='showcampaigns'),
    path('showcampaignlist/', views.showcampaignlists, name='showcampaignlist'),
    
    path('addinfluencertolist/<int:id>/', views.addinfluencertolist, name='addinfluencertolist'),
    path('removeinfluencerfromlist/<int:id>/<int:list_id>/', views.removeinfluencerfromlist, name='removeinfluencerfromlist'),
    path('viewinfluencerlist/<int:id>/', views.viewinfluencerlist, name='viewinfluencerlist'),
    path('allinfluencerslist/', views.allinfluencerslist, name='allinfluencerslist'),


    path('expandcard/',views.show_user_details, name = 'expand'),
    path('campaign_creators/<int:id>', views.campaign_creators, name='campaign_creators'),
    path('assigned_details/<int:id>', views.assigned_details, name='assgined_details'),
    path('add_deliverable/<int:id>', views.add_deliverable, name='add_deliverable'),
    path('view_deliverables/<int:id>', views.view_deliverables, name='view_deliverables'),
    path('content_review/<int:id>', views.content_review, name='content_review'),
    path('accept_review/<int:id>', views.accept_review, name= 'accept_review'),

    # path('marketer_campaign/<int:id>', views.marketer_campaign, name='marketer_campaign'),
    # path('view_list/<int:id>', views.view_list, name='view_list'),
    # path('assigned_campaign_detail/<int:id>', views.assigned_campaign_detail, name='assigned_campaign_detail'),
    # path('algolia/', views.algolia_search, name='algolia')
    # path('addcampaigntolist<int:id>/', views.addcampaigntolist, name='addcampaigntolist'),
    # path('addinfluencertolist/<int:id>/',views.addinfluencertolist, name='addinfluencertolist'),
    # path('addprofiletolist/', views.Addprofiletolist, name='addprofiletolist'),
    # path('show_profiles/', views.show_profiles, name='showcprofiles'),
    # path('showinfluencers/', views.show_influencer, name='showinfluencers'),

]