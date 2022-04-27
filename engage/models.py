from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


def platforms():
    return ['Instagram', 'Facebook', 'Youtube', 'Twitter']

class JobCreationCharges(models.Model):
    gig_extra = models.IntegerField(default=0)
    direct_offer_extra = models.IntegerField(default=0)

class GigPaymentID(models.Model):
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    payment_amount = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
class Gig(models.Model):
    marketer_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    open_for_bidding = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    start_date_bid = models.DateTimeField(null=True, blank=True)
    end_date_bid = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    final_amount = models.FloatField(null=True, blank=True)
    platforms = ArrayField(models.CharField(max_length=9, blank=True, null=True), size=4, default=platforms)
    paid_for = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    payment_id = models.ForeignKey(GigPaymentID, null=True, blank=True, on_delete=models.CASCADE)
    location_preferences = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)

    def __str__(self):
        return str(self.name)

class DirectOfferPaymentID(models.Model):
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    payment_amount = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)

class DirectOffer(models.Model):
    gig_id = models.ForeignKey(Gig, null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, blank=True)
    expires = models.DateTimeField(null=True, blank=True)
    paid_for = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    payment_id = models.ForeignKey(DirectOfferPaymentID, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)

class Dispute(models.Model):
    gig_id = models.ForeignKey(Gig, null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='dispute_against')
    against = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
