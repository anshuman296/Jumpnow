from accounts.models import SocialMedia, TwitterData, YoutubeData, UserProfile, LoggedInUser
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import HttpResponse
from post_office import mail
from django.conf import settings
import json


from accounts.process_social_data import process_twitter_data
from accounts.slack_bot import send_celebrity_sign_up_notification

@receiver(user_logged_in)
def user_logged_in_social(request, user, **kwargs):
    print(user, "*****************")

@receiver(social_account_added)
def user_social_account_added(request, sociallogin, **kwargs):
    user = sociallogin.user
    print(sociallogin.user, "$$$$$$$$$$$$")
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    if userprofile:
        socialprofile, create_social = SocialMedia.objects.get_or_create(profile=userprofile)
        socialprofile.save()
        
        if socialprofile:
            scs = user.socialaccount_set.all()
            for sc in scs:
                print(sc)
                if sc.provider == 'twitter':
                    username = sc.extra_data['screen_name']
                    print(username)
                    processed_data = process_twitter_data(socialprofile, sc)
                    
                    twitter_profile, twitter_profile_created = TwitterData.objects.get_or_create(**processed_data)
                    if twitter_profile_created:
                        if socialprofile.connected_profiles:
                            socialprofile.connected_profiles.append('twitter')
                        else:
                            socialprofile.connected_profiles = ['twitter']
                        socialprofile.tags.add('twitter', username)
                        socialprofile.save()

@receiver(post_save, sender=YoutubeData)
def check_for_celebrity(sender, instance, created, update_fields, **kwargs):
    if instance.subscribers > 50000:
        print(send_celebrity_sign_up_notification(instance.social_profile))

@receiver(post_save, sender=TwitterData)
def check_for_celebrity(sender, instance, created, update_fields, **kwargs):
    if instance.followers > 50000:
        print(send_celebrity_sign_up_notification(instance.social_profile))

@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
