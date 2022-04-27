from engage.models import Gig, DirectOffer, Dispute
from django import forms

class NewGigForm(forms.ModelForm):

    class Meta:
        model = Gig
        fields = '__all__'

class NewDOForm(forms.ModelForm):

    class Meta:
        model = DirectOffer
        fields = '__all__'

class NewDisputeForm(forms.ModelForm):

    class Meta:
        model = Dispute
        fields = '__all__'