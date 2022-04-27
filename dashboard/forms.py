from django import forms
from .models import Inquiry
from discovery.models import AssignedCreators
from django.forms import ModelForm



class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('user_type', 'email')


