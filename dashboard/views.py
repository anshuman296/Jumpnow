from django.shortcuts import render
from accounts.decorators import *
from django.contrib.auth.decorators import login_required
from accounts.models import SocialMedia
from .models import Inquiry
from .forms import InquiryForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from accounts.models import *
from discovery.models import *
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import uuid
from jumpnow.settings.base import EMAIL_HOST_USER


# @complete_profile
def main(request):
    return render(request, 'dashboard/index.html')

def index_form(request):
    user_type= request.POST['user_type']
    url_mail = request.POST['url_email']
    if request.method== "POST":
        data = Inquiry.objects.create(email= url_mail, user_type= user_type )
        data.save()
        if user_type == 'creator':
            return redirect('register_creator')
        else:
            return redirect('register')
    else:
        return redirect('dashboard_main')




class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# def verify_email(request):
#         user = request.user
#         print(user)
#         cur_user= UserProfile.objects.get(user=request.user)
#         print(cur_user)

#         p_email = cur_user.business_email
#         print(p_email)
#         current_site = get_current_site(request)
#         mail_subject = 'Activate your blog account.'
#         message = render_to_string('dashboard/acc_active_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             'token':account_activation_token.make_token(user),
#         })
#         email = EmailMessage(
#                     mail_subject, message, to=[p_email]
#         )
#         email.content_subtype = "html" 

#         email.send()
#         print(message)
#         return HttpResponse('Please confirm your email address to complete the registration')
#         # context={'user_form': user_form,'profile_form':profile_form,'contact_form':contact_form}
def verify_email(request):
    print("In entry")
    auth_token = str(uuid.uuid4())
    profile_obj = UserProfile.objects.get(user=request.user)
    email = str(profile_obj.business_email)
    profile_obj.auth_token = auth_token
    profile_obj.save()
    send_mail_after_registration(email, auth_token)
    return redirect('/token')


def success(request):
    return render(request, 'dashboard/success.html')


def error_page(request):
    return render(request, 'dashboard/error.html')


def token_send(request):
    return render(request, 'dashboard/token_send.html')


# @login_required(login_url='/')
def creator_dashboard(request):
    print("In creator dashboard")
    context = {}
    try:
        connected_accounts = SocialMedia.objects.get(profile=request.user.profile).connected_profiles
        context['connected_accounts'] = connected_accounts
        print(context)
    except:
        print("Some error")
        print("In creator dashboard")

    # user_form = User.objects.get(username=request.user)
    user_form = get_object_or_404(User, username=request.user)
    profile_form = get_object_or_404(UserProfile, user=request.user)
    contact_form = get_object_or_404(Contact, user_profile__user=request.user)
    if request.method == 'POST':
        user_name = request.POST['user_name'].split(" ")
        first_name = user_name[0]
        last_name = user_name[1]
        print(first_name, last_name)
        bio = request.POST['bio']
        tags = request.POST.getlist('tags')
        dob = request.POST['dob']
        gender = request.POST['gender']
        print('gender', gender)
        location = request.POST['location']
        mobile_no = request.POST['mobile_no']
        email = request.POST['email']
        if user_name:
            User.objects.filter(username=request.user).update(first_name=first_name, last_name=last_name)
        # if mobile_no:
        #     Contact.objects.filter(user_profile__user=request.user).update(mobile_number= mobile_no)
        if bio and tags and dob and gender and location:
            UserProfile.objects.filter(user=request.user).update(bio=bio, dob=dob, gender=gender, location=location,
                                                                 tags=tags)
            ######################### mail system ####################################
        auth_token = str(uuid.uuid4())
        context = {'user_form': user_form, 'profile_form': profile_form, 'contact_form': contact_form}
    else:
        context = {'user_form': user_form, 'profile_form': profile_form, 'contact_form': contact_form}
    print(context)
    print(context['profile_form'].bio)

    return render(request, 'dashboard/dashboard.html', context)


def inquiry_data(request):
    context = {}
    form = InquiryForm(request.POST)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context['form'] = form
    return render(request, 'dashboard/index.html', context)


def send_mail_after_registration(email, token):
    print('In send mail')
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    # send_mail(subject, message , email_from ,recipient_list,fail_silently=False )
    send_mail(subject, message, 'nikhileshcherukuri2@gmail.com', ['nikhilesh.cherukuri001@gmail.com'],
              fail_silently=False)
    print("sent")


def verify(request, auth_token):
    try:
        print("In verify token profile")
        profile_obj = UserProfile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/creator/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def assigned_campaigns(request):
    user = request.user
    campaigns = Campaign.objects.filter(assigned_creators__user_profile=user.profile.id)
    
    return render(request, 'dashboard/assigned_campaigns.html', {'campaigns': campaigns,})


def campaign_details(request, id):
    user = request.user
    context = {}
    context['campaign'] = Campaign.objects.prefetch_related('assigned_creators').get(id=id)
    context['assigned'] = context['campaign'].assigned_creators.get(user_profile=user.profile)
    return render(request, 'dashboard/campaign_details.html', context)


def campaign_requests(request):
    user = request.user
    campaigns = Campaign.objects.filter(assigned_creators__user_profile=user.profile, assigned_creators__accepted=False,
                                        assigned_creators__rejected=False)
    return render(request, 'dashboard/campaign_requests.html', {'campaigns': campaigns})




def accept_campaign(request, id):
    user = request.user
    campaigns = Campaign.objects.get(id=id, assigned_creators__user_profile=user.profile,
                                     assigned_creators__accepted=False, assigned_creators__rejected=False)
    campaigns.assigned_creators.update(accepted=True)
    campaigns.save()
    messages.info(request, 'Campaign accepted')
    return redirect('accepted_campaigns')


def accepted_campaigns(request):
    user = request.user
    campaigns = Campaign.objects.filter(assigned_creators__user_profile=user.profile, assigned_creators__accepted=True,
                                        assigned_creators__rejected=False)
    return render(request, 'dashboard/accepted_campaigns.html', {'campaigns': campaigns})


def budget_negotiation(request, id):
    assigned = AssignedCreators.objects.get(id=id)
    amount = request.POST.get('amount')
    if assigned.requested_amount == False and assigned.settled == False:
        if request.method == 'POST':
            assigned.request_budget = amount
            assigned.requested_amount = True
            assigned.offered_amount = False
            assigned.save()
        return HttpResponse('Amount offered.. Waiting for response !!')
    elif assigned.offered_amount == False and assigned.settled == False:
        if request.method == 'POST':
            assigned.offered_budget = amount
            assigned.requested_amount = False
            assigned.offered_amount = True
            assigned.save()
        return HttpResponse('. Waiting for response !!')
    else:
        return HttpResponse('Amount already settled')

    # return redirect('accepted_campaigns')


def settle_amount(request, id):
    assigned = AssignedCreators.objects.get(id=id)
    amount = request.POST.get('amount')
    print(amount)

    if assigned.requested_amount == False and assigned.settled == False:
        if request.method == 'POST':
            assigned.settled_amount = amount
            assigned.settled = True
            assigned.offered_amount = True
            assigned.requested_amount = True
            assigned.save()
        return HttpResponse('Amount settled')
    elif assigned.offered_amount == False and assigned.settled == False:
        if request.method == 'POST':
            assigned.settled_amount = amount
            assigned.settled = True
            assigned.offered_amount = True
            assigned.requested_amount = True
            assigned.save()
        return HttpResponse('Amount settled')
    else:
        return HttpResponse('Something went wrong')


#
def show_deliverables(request, id):
    assigned_creator = AssignedCreators.objects.get(id=id)
    deliverable = assigned_creator.deliverables.all()
    return render(request, 'dashboard/show_deliverables.html', {'deliverable': deliverable,
                                                                'assigned_creator': assigned_creator})


def content_creation(request, id):
    deliver = Deliverables.objects.get(id=id)
    image = request.FILES.get('filename', False)
    if request.method == 'POST':
        deliver.screenshot = image
        deliver.review_sent = True
        deliver.save()
        return HttpResponse('Content succesfully sent for review')
    return render(request, 'dashboard/content_creation.html', {'deliverable': deliver})

def deliverable_done(request, id):
    deliver = Deliverables.objects.get(id=id)
    confirmation_url = request.POST.get('confirmation_url')
    if request.method == 'POST':
        if not deliver.completed:
            deliver.confirmation_url = confirmation_url
            deliver.completed = True
            deliver.save()
            return HttpResponse('Submitted Successfully')
    return HttpResponse('Bad Request')



def profiles(request):
    return render(request, 'dashboard/profiles.html')


def creator(request):
    return render(request, 'dashboard/dashboard.html')

def socials(request):
    return render(request, 'dashboard/socials.html')

def home_page(request):
    return render(request, 'dashboard/landingPage_2.html')