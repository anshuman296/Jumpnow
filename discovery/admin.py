from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Subscription)
admin.site.register(DiscoveryProfile)
admin.site.register(Campaign)
admin.site.register(campaignList)
admin.site.register(SubscriptionPayments)
admin.site.register(AssignedCreators)
admin.site.register(Deliverables)

