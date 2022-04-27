from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.db.models import fields
from discovery.models import Contact, UserProfile, Campaign, campaignList



class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('campaign_name', 'user', 'campaign_list','campaign_description','bidding', 'offered_amount')
#
class CampaignListForm(forms.ModelForm):
    class Meta:
        model = campaignList
        fields = ('list_name','platform')









