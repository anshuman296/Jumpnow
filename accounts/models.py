from os import access
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField
from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords
from allauth.account.signals import user_logged_in
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from accounts.process_social_data import process_twitter_data
from django.core.files.storage import FileSystemStorage
from datetime import date
from django.apps import apps


# from discovery.models import Campaign

# apps.get_model('discovery.Campaign')


# from multiselectfield import MultiSelectField


@receiver(user_logged_in)
def user_logged_in_social(request, user, **kwargs):
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        socialprofile, create_social = SocialMedia.objects.get_or_create(profile=userprofile)
        socialprofile.save()

        if create_social:
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


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    LANGUAGE_CHOICES = ('EN', 'English'), ('HN', 'Hindi'), ('BN', 'Bengali'), ('UR', 'Urdu'), \
                       ('PN', 'Punjabi'), ('MR', 'Marathi'), ('TL', 'Telugu'), ('TM', 'Tamil'), \
                       ('GJ', 'Gujarati'), ('KN', 'Kannada'), ('OD', 'Odia'), ('ML', 'Malayalam'), \
                       ('AS', 'Assamese'), ('ST', 'Santali'), ('SK', 'Sanskrit')

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    # business_email = models.CharField(max_length=100, null=True, blank=True)
    business_email = models.EmailField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices= GENDER_CHOICES,  null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    dob = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='user_profile_image/')

    # age = models.IntegerField(null=True, blank=True)
    # ethnicity = models.CharField(max_length=100, null=True, blank=True)
    # tags = models.CharField(max_length=100, null= True, blank= True)
    relationship_status = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, null=True, blank=True)
    subscription = models.BooleanField(default=True, null=False, blank=False)
    mobile_number = models.CharField(max_length=15, null=True, blank=False)
    email_verified = models.BooleanField(default=False, null=False, blank=False)
    dark_mode = models.BooleanField(default=False, null=False)
    complete = models.BooleanField(default=False, null=False)
    creator = models.BooleanField(default=False, null=False)
    profile_image = models.ImageField(upload_to='marketer/', null=True, blank=True)
    registered = models.BooleanField(default=True, null=False)
    auth_token = models.CharField(max_length=100)

    @property
    def age(self):
        if (self.dob != None):
            age = date.today().year - self.dob.year
            return age

    def __str__(self):
        return str(self.user)


class BankDetail(models.Model):
    user_profile = models.OneToOneField(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    gst_no = models.CharField(max_length=15, null=True, blank=True)
    account_type = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_no = models.CharField(max_length=100, null=True, blank=True)
    account_no_ver = models.CharField(max_length=100, null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, null=True, blank=True)
    swift_code = models.CharField(max_length=100, null=True, blank=True)
    routing_code = models.CharField(max_length=100, null=True, blank=True)


class Contact(models.Model):
    user_profile = models.OneToOneField(UserProfile, null=True, blank=True, on_delete=models.CASCADE,
                                        related_name='contact')
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    address_line_2 = models.CharField(max_length=500, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=False)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.mobile_number


class SocialMedia(models.Model):
    profile = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE, related_name='social')
    contact_id = models.ForeignKey(Contact, null=True, on_delete=models.CASCADE, related_name='contact')
    connected_profiles = ArrayField(models.CharField(max_length=10, blank=True), null=True, blank=True)
    celebrity = models.BooleanField(default=False, null=False)
    jumpnow_score = models.IntegerField(default=0, null=True, blank=True)
    featured = models.BooleanField(default=False, null=False)
    featured_text = models.TextField(null=True, blank=True)
    featured_image = models.CharField(null=True, blank=True, max_length=500)
    tags = TaggableManager()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.profile.user.username)


def ig_profile_pic(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'media/user_{0}/{1}'.format(instance.instagram_id, filename)


class InstagramData(models.Model):
    social_profile = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='instagram')
    json_data = JSONField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    instagram_id = models.BigIntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    posts = models.BigIntegerField(null=True, blank=True)
    followers = models.BigIntegerField(null=True, blank=True)
    followings = models.BigIntegerField(null=True, blank=True)
    likes = models.BigIntegerField(null=True, blank=True)
    comments = models.BigIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    engagement_rate = models.FloatField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField(upload_to=ig_profile_pic, null=True, blank=True)
    history = HistoricalRecords()
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{str(self.username)}'

    class Meta:
        ordering = ['-username']


class WebsiteData(models.Model):
    social_profile = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='website')
    username = models.CharField(max_length=200, null=True, blank=True)


class TwitterData(models.Model):
    social_profile = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='twitter')
    json_data = JSONField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    followers = models.BigIntegerField(null=True, blank=True, default=0)
    retweets = models.BigIntegerField(null=True, blank=True)
    replies = models.BigIntegerField(null=True, blank=True)
    engagement_rate = models.FloatField(null=True, blank=True)
    history = HistoricalRecords()
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{str(self.username)}'


class FacebookData(models.Model):
    social_profile = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='facebook')
    json_data = JSONField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{str(self.username)}'


class YoutubeAuth(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='youtube_auth')
    token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    token_uri = models.TextField(null=True, blank=True)
    client_id = models.TextField(null=True, blank=True)
    client_secret = models.TextField(null=True, blank=True)
    scopes = models.TextField(null=True, blank=True)


class YoutubeData(models.Model):
    social_profile = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='youtube')
    json_data = JSONField(null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    channel_name = models.CharField(max_length=100, null=True, blank=True)
    channel_id = models.CharField(max_length=100, null=True, blank=True)
    subscribers = models.BigIntegerField(null=True, blank=True)
    videoCount = models.BigIntegerField(null=True, blank=True)
    viewCount = models.BigIntegerField(null=True, blank=True)
    avgViews = models.FloatField(null=True, blank=True)
    engagement_rate = models.FloatField(null=True, blank=True)
    history = HistoricalRecords()
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{str(self.username)}'


# class AcceptedCampaign(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
#     campaign = models.OneToOneField('discovery.Campaign', on_delete=models.CASCADE, null=True, blank=True )
#     request_amount = models.IntegerField(default=0, null=True, blank=True)


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,
                                related_name='logged_in_user')
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.Username


class Instagram_temp_data(models.Model):
    user_profile = models.OneToOneField(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length= 100, null= True, blank= True)