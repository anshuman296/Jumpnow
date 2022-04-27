from django.urls import path
from django.conf.urls import url, include
from dashboard import views
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('login/', views.Login, name='index'),
    path('register/', views.RegisterLanding, name='register_landing'),
    path('register/user', views.Register, name='register'),
    path('register/creator', views.RegisterCreator, name='register_creator'),
    path('register/creator/connect_accounts', views.social_connect, name='social_connect'),
    path('register/userprofile/', views.userprofiledata, name='userprofile'),

    path('bank_details/', views.bank_details, name= 'bank_details'),
    path('insta_temp/', views.insta_temp, name='insta_temp'),
    path('terms_conditions/', views.terms_conditions, name='tnc'),

    # path('register/user/redirect', views.register_user_redirect, name='register_user_redirect'),
    path('logout/', views.Logout, name='logout'),
    path('oauth/', include('social_django.urls', namespace="social")),
    path('resendmail/',views.resendmaillink, name='resendmail'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),

    path('connect/instagram', views.instagram_connect, name='instagram_connect'),
    path('connect/facebook', views.facebook_connect, name='facebook_connect'),

    path('connect/twitter', views.twitter_connect, name='twitter_connect'),
    path('connect/youtube', views.youtube_connect, name='youtube_connect'),
    path('connect/tags', views.tags_connect, name='tags_connect'),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/reset_password/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_password/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_password/password_reset_done.html"), 
        name="password_reset_complete"),
    
    path('google/oauth2callback/', views.GoogleOauth2Callback, name='gauth_callback'),

    # path('get_facebook_data/',views.get_facebook_data, name='get_facebook_data'),
    url('social-auth/', include('social_django.urls', namespace='social')),


  
  
#    path('get_facebook_data/',views.get_facebook_data, name='get_facebook_data'),
#    path('oauth/', include('social_django.urls', namespace='social')),
#    path('algolia/', views.algolia_search, name='algolia')
#    path('get_facebook_data/',views.get_facebook_data, name='get_facebook_data'),
#     path('algolia/', views.algolia_search, name='algolia')
#     path('facebook/', views.get_facebook_data, name= 'facebook')
#     path('algolia/', views.algolia_search, name='algolia')




]