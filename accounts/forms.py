from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model,User
from django.db.models import fields
from accounts.models import Contact, UserProfile


GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        widgets = {
            'username': forms.EmailInput(attrs={
                'placeholder': 'Email',
            }),
            'email': forms.HiddenInput,
        }

    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()

        return user


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('business_email', 'gender', 'bio', 'age', 'ethnicity',
#                   'relationship_status', 'education', 'language', 'profile_image',)


TAGS_OPTIONS = (
        ("Arts", "Arts"),
        ("Fashion", "Fashion"),
        ("Food", "Food"),
       )
class UserProfileForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=TAGS_OPTIONS,
       )
    class Meta:
        model = UserProfile
        fields = ['gender', 'bio', 'dob', 'location']
        
                    
        widgets = {

            'gender': forms.Select(attrs={
                'placeholder': 'Gender'
            }),
            'bio': forms.TextInput(attrs={
                'placeholder': 'Bio'
            }),
            'locations': forms.TextInput(attrs={
                'placeholder': 'Location'
            }),
            'dob': forms.DateInput(attrs={
                'placeholder': 'DOB'
            }),
            # 'tags': forms.CheckboxSelectMultiple(attrs={
            #     'placeholder': 'Select tags','choices':TAGS_OPTIONS
            # }),
                                          

        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['user_profile']

class MobileNoForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['mobile_number']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username']
