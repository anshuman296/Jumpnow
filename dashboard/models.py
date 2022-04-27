from django.db import models
from django.conf import settings
from accounts.models import UserProfile
from discovery.models import Campaign, DiscoveryProfile


# Create your models here.



class Inquiry(models.Model):
    user_type = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.email)





