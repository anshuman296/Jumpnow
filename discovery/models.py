from django.db import models
from accounts.models import *
from django.utils import timezone


# Create your models here.

class Subscription(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    searches = models.IntegerField(default=0, null=True, blank=True)
    exports = models.IntegerField(default=0)
    razorpay_sub_id = models.CharField(max_length=100, null=True, blank=True)


class DiscoveryProfile(models.Model):
    profile = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE, related_name='discovery')
    budget = models.IntegerField(null=True, blank=True)
    free_searches = models.IntegerField(default=5, null=False, blank=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    subscription_searches = models.IntegerField(default=0, null=False, blank=False)
    exports_done = models.IntegerField(default=0, null=True, blank=True)
    exports_max = models.IntegerField(default=5, null=True, blank=True)
    searches_done = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return str(self.profile)


class SubscriptionPayments(models.Model):
    discovery_profile = models.ForeignKey(DiscoveryProfile, null=True, on_delete=models.CASCADE,
                                          related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    valid_till = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)


class campaignList(models.Model):
    PLATFORM_CHOICES = (
        ("YouTube", "YouTube"),
        ("Instagram", "Instagram"),
        ("Facebook", "Facebook"),
        ("Twitter", "Twitter"),
    )
    user = models.ForeignKey(DiscoveryProfile, null=True, blank=True, on_delete=models.CASCADE,
                             related_name='campaign_list')
    list_name = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    profiles = models.ManyToManyField(SocialMedia, blank=True)
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    # def __str__(self):
    #     return self.list_name

class Content(models.Model):
    screenshot = models.ImageField(null=True, blank=True, upload_to='media/')
    content_url = models.TextField(null=True, blank=True)

class Deliverables(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    platform = models.CharField(max_length=100, null=True, blank=True)
    deliverable = models.CharField(max_length=100, null=True, blank=True)
    screenshot = models.ImageField(null=True, blank=True, upload_to='media/')
    content_url = models.TextField(null=True, blank=True)
    remark = models.TextField(max_length=200, null=True, blank=True)
    review_sent = models.BooleanField(default=False)
    review_accepted = models.BooleanField(default=False)
    confirmation_url = models.TextField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    content_review = models.ManyToManyField(Content, null=True, blank=True)


class AssignedCreators(models.Model):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    request_budget = models.IntegerField(default=0, null=True, blank=True)
    offered_budget = models.IntegerField(default=0, null=True, blank=True)
    settled_amount = models.IntegerField(default=0, null=True, blank=True)
    requested_amount = models.BooleanField(default=False)
    offered_amount = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    deliverables = models.ManyToManyField(Deliverables, null=True, blank=True)
    payment = models.BooleanField(default=False)
    rzrpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    rzrpay_payment_id = models.CharField(max_length=255, null=True, blank=True)


class Campaign(models.Model):
    user = models.ForeignKey(DiscoveryProfile, null=True, on_delete=models.CASCADE, related_name='campaign')
    campaign_name = models.CharField(max_length=255, null=True, blank=True)
    campaign_description = models.TextField(null=True, blank=True)
    campaign_deliverables = models.TextField(null=True, blank=True)
    bidding = models.BooleanField(default=True)
    campaign_list = models.ManyToManyField(campaignList, null=True, blank=True)
    offered_amount = models.IntegerField(default=0, null=True, blank=True)
    negotiation = models.IntegerField(default=0, null=True, blank=True)
    creator_status = models.BooleanField(default=False)
    marketer_status = models.BooleanField(default=False)
    creator_approved = models.BooleanField(default=False)
    marketer_approved = models.BooleanField(default=False)
    settled_amount = models.IntegerField(default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    assigned_creators = models.ManyToManyField(AssignedCreators, null=True, blank=True)

    def __str__(self):
        return str(self.campaign_name)