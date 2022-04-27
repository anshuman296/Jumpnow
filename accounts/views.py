from accounts.process_social_data import process_twitter_data, process_youtube_data, process_instagram_data
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from post_office import mail
from accounts.forms import *
from accounts.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.decorators import *
from accounts.social_api import *
from django.core import serializers
from django.db.models.signals import post_save
from discovery.models import *
from django.shortcuts import get_object_or_404
from datetime import date
from social_django.models import UserSocialAuth
import requests
from requests_oauthlib import OAuth1
import datetime


# from algoliasearch_django import raw_search


# from algoliasearch_django import raw_search


# @unauthenticated_user
def RegisterLanding(request):
    # print(get_tiktok_user("hello"))
    return render(request, 'accounts/registerLanding.html')


def social_login_cancelled(request):
    return redirect('index')


# @unauthenticated_user
def Register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            userprofile = UserProfile.objects.create(user=newuser)
            phone = request.POST.get('mobile_number')
            userprofile = UserProfile.objects.get(user=newuser)
            userprofile.mobile_number = phone
            userprofile.save()
            contact_profile = Contact.objects.create(user_profile=userprofile, mobile_number=phone)
            newuser.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/email/acc_activation.html', {
                'user': newuser,
                'domain': settings.URL_BACKEND,
                'uid': urlsafe_base64_encode(force_bytes(newuser.pk)),
                'token': default_token_generator.make_token(newuser),
            })
            to_email = form.cleaned_data.get('username')
            marketer_group = Group.objects.get(name='marketer')
            marketer_group.user_set.add(newuser)
            discovery_profile = DiscoveryProfile.objects.create(profile=userprofile)
            discovery_profile.save()
            mail.send(
                [to_email],
                subject=mail_subject,
                sender=settings.EMAIL_HOST_USER,
                message=message,
                priority='now',
            )
            messages.success(request, "You've successfully registered!")
            messages.info(request,
                          "Please verify your email address, we've sent you a mail at your registered email ID.")
            print('user created', newuser)
            # return redirect('index')
            return render(request, 'accounts/template_page.html')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'accounts/register_marketer.html', {'form': form})


@unauthenticated_user
def RegisterCreator(request):
    print("HELLO REGISTER IS HERE")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            userprofile = UserProfile.objects.create(user=newuser)
            phone = request.POST.get('mobile_number')
            userprofile = UserProfile.objects.get(user=newuser)
            userprofile.mobile_number = phone
            userprofile.creator = True
            userprofile.save()
            newuser.save()
            contact_profile = Contact.objects.create(user_profile=userprofile, mobile_number=phone)
            socialprofile = SocialMedia.objects.create(profile=userprofile, contact_id=contact_profile)
            socialprofile.save()
            data = BankDetail.objects.create(user_profile=userprofile)
            data.save()
            insta_temp = Instagram_temp_data.objects.create(user_profile=userprofile)
            insta_temp.save()
            current_site = get_current_site(request)
            creator_group = Group.objects.get(name='creator')
            creator_group.user_set.add(newuser)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/email/acc_activation.html', {
                'user': newuser,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(newuser.pk)),
                'token': default_token_generator.make_token(newuser),
            })
            to_email = form.cleaned_data.get('username')
            mail.send(
                [to_email],
                subject=mail_subject,
                sender=settings.EMAIL_HOST_USER,
                message=message,
                priority='now',
            )
            messages.info(request,
                          "Please verify your email address to proceed, we've sent you a mail at your registered email ID.")
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'accounts/register_creator.html', {'form': form})


def activate(request, uidb64, token):
    print('hiiiii')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print('user', user)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        userprofile = UserProfile.objects.get(user=user)
        userprofile.email_verified = True
        userprofile.save()
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')


@unauthenticated_user
def Login(request):
    print("In Login")
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            userprofile = UserProfile.objects.get(user=user)
            if (userprofile.email_verified == settings.EMAIL_VALIDATION) or (userprofile.email_verified):
                login(request, user)
                print(userprofile.creator)
                if user.profile.creator:
                    return redirect('dashboard_new')
                else:
                    return redirect('discovery_search')
            else:
                messages.error(request, 'Please confirm your email address.')
        else:
            messages.error(request, 'Username or password is incorrect.')

    return render(request, 'accounts/login.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['creator'])
def social_connect(request):
    context = {}
    try:
        connected_accounts = SocialMedia.objects.get(profile=request.user.profile).connected_profiles
        context['connected_accounts'] = connected_accounts
        print(context)
    except:
        print("Some error")
    return render(request, 'accounts/social_connect.html', context)


# @login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('index')


def count_hit(request, object, context):
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    return hitcontext


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['creator'])
def instagram_connect(request):
    if request.method == 'POST':
        username = request.POST['instagram-username']
        print(request.user, "logged in user is here")
        user_social_media_profile = SocialMedia.objects.get(profile=request.user.profile)
        user_data = get_instagram_userid(username)
        # processed_data = process_instagram_data(username, user_data, follower)
        # print(processed_data)
        insta_location = UserProfile.objects.get(user=request.user)
        insta_profile, insta_profile_created = InstagramData.objects.get_or_create(
            username=username,
            social_profile=user_social_media_profile,
            json_data=user_data,
            location=insta_location.location
            # followers= user_data['follower'],
            # followings=user_data['following'],
            # instagram_id= user_data['id'],
            # posts=user_data['total_post'],
            # likes=user_data['average_like'],
            # comments=user_data['average_comment'],
            # is_verified= user_data['is_verified'],
            # bio= user_data['biography'],
            # full_name= user_data['full_name']

        )

        if insta_profile_created:
            if user_social_media_profile.connected_profiles:
                user_social_media_profile.connected_profiles.append('instagram')
            else:
                user_social_media_profile.connected_profiles = ['instagram']
            user_social_media_profile.tags.add('instagram', username)
            user_social_media_profile.save()

        print(user_data)
        # response = serializers.serialize("json", )
        print("done")
    return JsonResponse({"hello": "hello"}, status=200)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['creator'])
def twitter_connect(request):
    # twitter_login = request.user.social_auth.get(provider='twitter')
    twitter_login = UserSocialAuth.objects.get(provider='twitter')

    print("******")
    print(twitter_login.extra_data)
    start_date = datetime.datetime.utcnow() - datetime.timedelta(30)
    start_time = start_date.replace(microsecond=0).isoformat("T") + "Z"
    print(start_time)

    twitter_uid = twitter_login.extra_data["id"]
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAIGNVAEAAAAAQpBgaGRJ4413hc9iSRA%2BdgHeVmc%3DakIKfNNRbE0Yrurb5H8sghaDqm5lzyYWXcFa9QS4mFZyEICANX"
    resp_username = requests.get(f'https://api.twitter.com/2/users/{twitter_uid}?user.fields=location',
                                 headers={'Authorization': 'Bearer {}'.format(bearer_token)})

    uname = resp_username.json()
    print(uname)

    profile_obj = UserProfile.objects.get(user=request.user)
    location = str(uname['data']['location'])
    profile_obj.location = location
    profile_obj.save()

    resp = requests.get(f'https://api.twitter.com/2/users/{twitter_uid}/tweets?start_time={start_time}',
                        headers={'Authorization': 'Bearer {}'.format(bearer_token)})
    user_tweets_objs = resp.json()
    print("******")

    print(user_tweets_objs)
    if user_tweets_objs['meta']['result_count'] != 0:
        user_tweet_ids = [ob['id'] for ob in user_tweets_objs["data"]]

        YOUR_APP_KEY = "lYiH14idCH5rz5S5Q2QisNPcJ"
        YOUR_APP_SECRET = "ELR4UOzasBhxIVax75hyySBpvnb6YLZCS8fwTBZhzcEjdF1smr"
        USER_OAUTH_TOKEN = twitter_login.extra_data["access_token"]["oauth_token"]
        USER_OAUTH_TOKEN_SECRET = twitter_login.extra_data["access_token"]["oauth_token_secret"]

        print(USER_OAUTH_TOKEN)

        all_tweet_engagements = []
        print(user_tweet_ids)
        auth = OAuth1(YOUR_APP_KEY, YOUR_APP_SECRET, USER_OAUTH_TOKEN, USER_OAUTH_TOKEN_SECRET)
        for tid in user_tweet_ids:
            eng_data = requests.get(
                f'https://api.twitter.com/2/tweets/{tid}?tweet.fields=non_public_metrics,organic_metrics&media.fields=non_public_metrics,organic_metrics&expansions=attachments.media_keys',
                auth=auth)
            format_data = eng_data.json()
            all_tweet_engagements.append(format_data)

        print(all_tweet_engagements)
        init_engage = 0
        for tw in all_tweet_engagements:
            init_engage += (tw['data']['organic_metrics']['user_profile_clicks'] + tw['data']['organic_metrics'][
                'reply_count'] + tw['data']['organic_metrics']['retweet_count'] + tw['data']['organic_metrics'][
                                'like_count']) / tw['data']['organic_metrics']['impression_count']

        print(init_engage / len(all_tweet_engagements))
        eng_rate = init_engage / len(all_tweet_engagements)

        send_json = {}
        send_json['authtokens'] = twitter_login.extra_data
        send_json['engage'] = all_tweet_engagements

        TwitterData.objects.create(
            username=twitter_login.extra_data["access_token"]["screen_name"],
            social_profile=SocialMedia.objects.get(profile=request.user.profile),
            name=uname["data"]["name"],
            json_data=send_json,
            engagement_rate=eng_rate

        )

    if request.method == 'POST':
        username = request.POST['twitter-username']
        user_social_media_profile = SocialMedia.objects.get(profile=request.user.profile)

        user_data = get_twitter_data(username)
        # processed_data = process_twitter_data(username, user_social_media_profile, user_data)
        # print(processed_data)
        twitter_location = UserProfile.objects.get(user=request.user)
        twitter_profile, twitter_profile_created = TwitterData.objects.get_or_create(
            username=username,
            social_profile=user_social_media_profile,
            json_data=user_data,
            location=twitter_location.location

        )
        if twitter_profile_created:
            if user_social_media_profile.connected_profiles:
                user_social_media_profile.connected_profiles.append('twitter')
            else:
                user_social_media_profile.connected_profiles = ['twitter']
            user_social_media_profile.tags.add('twitter', username)
            user_social_media_profile.save()
        # response = serializers.serialize("json", )
        print("done")
    return JsonResponse({"hello": "hello"}, status=200)


# @login_required(login_url='/')
# # #@allowed_users(allowed_roles=['creator'])
# def youtube_connect(request):
#     if request.method == 'POST':
#         username = request.POST['youtube-username']
#         print(request.user, "logged in user is here")
#         user_social_media_profile = SocialMedia.objects.get(profile=request.user.profile)
#         user_data = get_youtube_data(username)
#         processed_data = process_youtube_data(username, user_social_media_profile, user_data)
#         youtube_profile, youtube_profile_created = YoutubeData.objects.get_or_create(**processed_data)
#         if youtube_profile_created:
#             if user_social_media_profile.connected_profiles:
#                 user_social_media_profile.connected_profiles.append('youtube')
#             else:
#                 user_social_media_profile.connected_profiles = ['youtube']
#             user_social_media_profile.tags.add('youtube', username)
#             user_social_media_profile.save()
#         print(user_data)
# #         # response = serializers.serialize("json", )
#         print("done")
#     return JsonResponse({"hello": "hello"}, status=200)

@login_required(login_url='login')
def youtube_connect(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
        scopes=['https://www.googleapis.com/auth/youtube.readonly'])

    flow.redirect_uri = f'{settings.URL_BACKEND}/google/oauth2callback/'

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    # return JsonResponse({"auth_url": authorization_url, "state": state}, status=200)
    return redirect(authorization_url, state)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


@login_required(login_url='login')
def GoogleOauth2Callback(request):
    if request.method == 'GET':
        state = request.GET.get('state', False)
        code = request.GET.get('code', False)
        scope = request.GET.get('scope', False)

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON, scopes=scope, state=state
        )

        flow.redirect_uri = f'{settings.URL_BACKEND}/google/oauth2callback/'

        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        dict_credentials = credentials_to_dict(credentials)

        ytauth, created = YoutubeAuth.objects.get_or_create(user_id=request.user)
        ytauth.token = dict_credentials["token"]
        ytauth.refresh_token = dict_credentials["refresh_token"]
        ytauth.token_uri = dict_credentials["token_uri"]
        ytauth.client_id = dict_credentials["client_id"]
        ytauth.client_secret = dict_credentials["client_secret"]
        ytauth.scopes = dict_credentials["scopes"]

        ytauth.save()
        if ytauth:
            user_social_media_profile = SocialMedia.objects.get(profile=request.user.profile)
            user_data = get_youtube_data(request.user)
            processed_data = process_youtube_data(user_social_media_profile, user_data)
            youtube_profile, youtube_profile_created = YoutubeData.objects.get_or_create(
                social_profile=user_social_media_profile)
            youtube_profile.__dict__.update(processed_data)
            youtube_profile.save()
            if youtube_profile_created:
                if user_social_media_profile.connected_profiles:
                    user_social_media_profile.connected_profiles.append('youtube')
                else:
                    user_social_media_profile.connected_profiles = ['youtube']
                user_social_media_profile.tags.add('youtube')
                user_social_media_profile.save()
    return redirect('dashboard_new')


@login_required
def InstagramCallback(request):
    if request.method == 'GET':
        code = request.GET.get('code', False)
        flow = f'https://api.instagram.com/oauth/access_token\client_id=433525035178851\client_secret=dfeb735cdb15aee2a2abf9bc4fbb1398\grant_type=authorization_code\redirect_uri=https://app.jumpnow.agency/\code={code}'


@login_required(login_url='login')
def tags_connect(request):
    if request.method == 'GET':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        media_profile = SocialMedia.objects.get(profile=profile)
        social_tags = list(media_profile.tags.names())
        return JsonResponse({'tags': social_tags})
    elif request.method == 'POST':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        media_profile = SocialMedia.objects.get(profile=profile)
        new_tags = json.loads(request.body)
        new_tags = new_tags['new_tags']
        media_profile.tags.clear()
        for tag in new_tags:
            media_profile.tags.add(tag)
        media_profile.save()
        return JsonResponse({'status': 'Success'})


@login_required(login_url='/')
def resendmaillink(request):
    # obj = get_object_or_404(UserProfile, user=request.user)
    newuser = request.user
    current_site = get_current_site(request)
    # creator_group = Group.objects.get(name='creator')
    # creator_group.user_set.add(newuser)
    mail_subject = 'Activate your account.'
    message = render_to_string('accounts/email/acc_activation.html', {
        'user': newuser,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(newuser.id)),
        'token': default_token_generator.make_token(newuser),
    })
    # to_email = form.cleaned_data.get('username')
    to_email = newuser
    mail.send(
        [request.user.email],
        subject=mail_subject,
        sender=settings.EMAIL_HOST_USER,
        message=message,
        priority='now',
    )
    messages.info(request,
                  "Please Check your email, we've sent you a mail at your registered email ID.")
    return redirect('dashboard_new')


@login_required(login_url='login')
def userprofiledata(request):
    # context = {}
    # obj = get_object_or_404(UserProfile, user=request.user)
    # obj1 = get_object_or_404(User, username=request.user)
    # obj2 = get_object_or_404(Contact, user_profile__user=request.user)
    #
    # # if obj.email_verified == False:
    # #     messages.info(request,
    # #                       "Please verify your email address, Click here for Resend mail !!")
    # # else:
    # #     messages.info(request,
    # #                       "Your email address Verified")
    # profile_form = UserProfileForm(request.POST or None, instance=obj)
    # user_form = UserForm(request.POST or None, instance=obj1)
    # contact_form = MobileNoForm(request.POST or None, instance=obj2)
    # user_form.name_data = obj1.first_name + " " + obj1.last_name
    # if request.method == 'POST':
    #     profile_form = UserProfileForm(request.POST, instance=obj)
    #     user_form = UserForm(request.POST, instance=obj1)
    #     tags_list = request.POST.getlist('tags')
    #     print('forms', tags_list)
    #     if profile_form.is_valid() and user_form.is_valid():
    #         profile_form.tags = tags_list
    #         profile_form.save(commit=False)
    #         profile_form.save()
    #         user_form.save()
    #         return redirect('dashboard_new')
    #     else:
    #         messages.error(request, 'Please enter correct details')
    #
    # context["profile_form"] = profile_form
    # context["user_form"] = user_form
    # context["contact_form"] = contact_form
    # context['obj'] = obj
    # context['obj1'] = obj1
    # # context['name_data'] = user_form.name_data



    context = {}
    user = request.user
    f_name = request.POST.get('fname')
    l_name = request.POST.get('lname')
    gender = request.POST.get('gender')
    dob = request.POST.get('dob')
    location = request.POST.get('location')
    # phone = request.POST.get('name')
    # email = request.POST.get('name')
    user_data = User.objects.get(email=user.email)
    user_profile_data = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user_data.first_name = f_name
        user_data.last_name = l_name
        user_data.save()
        user_profile_data.gender = gender
        user_profile_data.dob = dob
        user_profile_data.location = location
        user_profile_data.save()

    context['user'] = user_data
    context['userprofile'] = user_profile_data
    return render(request, 'accounts/userprofile.html', context)
    # return render(request, 'accounts/userprofile_test.html', context)


@login_required(login_url='login')
def facebook_connect(request):
    print("In fb View")
    if request.method == 'POST':
        username = request.POST['facebook-username']
        # user_social_media_profile = SocialMedia.objects.get(profile=request.user.profile)
        # user_data = get_facebook_data(username)
        # processed_data = process_twitter_data(username, user_social_media_profile, user_data)
        # print(processed_data)
        # facebook_profile, facebook_profile_created = FacebookData.objects.get_or_create(
        #     username=username,
        #     social_profile=user_social_media_profile,
        #     # json_data=user_data,
        #     # followers= user_data["followers"]
        # )
        # if facebook_profile_created:
        #     if user_social_media_profile.connected_profiles:
        #         user_social_media_profile.connected_profiles.append('facebook')
        #     else:
        #         user_social_media_profile.connected_profiles = ['facebook']
        #     user_social_media_profile.tags.add('facebook', username)
        #     user_social_media_profile.save()
        # response = serializers.serialize("json", )
        print(user_data)
    return JsonResponse({"hello": "hello"}, status=200)


# def algolia_search(request):
#     response = raw_search(UserProfile, "jhabua")
#     return JsonResponse({"response": response})


# url: 'https://api.getshoutout.com/coreservice/messages'
# method: 'POST'
# headers: {
# 'Content-Type': 'application/json',
# 'Authorization': 'Apikey eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmZjdhMTMyMC0zMmU2LTExZWMtYjE1ZC00MWY1OWJmMWJjM2YiLCJzdWIiOiJTSE9VVE9VVF9BUElfVVNFUiIsImlhdCI6MTYzNDg3MjgyNSwiZXhwIjoxOTUwNDA1NjI1LCJzY29wZXMiOnsiYWN0aXZpdGllcyI6WyJyZWFkIiwid3JpdGUiXSwibWVzc2FnZXMiOlsicmVhZCIsIndyaXRlIl0sImNvbnRhY3RzIjpbInJlYWQiLCJ3cml0ZSJdfSwic29fdXNlcl9pZCI6IjYxMDQ1Iiwic29fdXNlcl9yb2xlIjoidXNlciIsInNvX3Byb2ZpbGUiOiJhbGwiLCJzb191c2VyX25hbWUiOiIiLCJzb19hcGlrZXkiOiJub25lIn0.TULUiHOgGhlpbm_Pk2TBn-HxcUfP_gfiIPXe7cN6bAE',
# }
# body: JSON.stringify({
# "source": "ShoutDEMO",
# "destinations": ["9767734458"],
# "transports": ["sms"],
# "content": {
# "sms": "Sent via ShoutOUT Gateway!!"
# }
# })


# account_sid = 'ACbdeccd93d234a3e9b49266501329b5d4'
# auth_token = '301089997690d74600ccdb30df3e7628'
# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                     body="Your Twilio verification code is 456987", Please ,
#                     from_='+13203968350',
#                     to='+919767734458'
#                 )

# print(message.sid)

# def sms_send(request):

#     conn = http.client.HTTPConnection("2factor.in")
#     randomOTP=random.randint(1111,9999)

#     conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=fc7c8fc8-3326-11ec-a13b-0200cd936042&to=7058933624&otpvalue="+str(randomOTP)+"&templatename=sendsimplesms")
#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))

#     return HttpResponse('send message')
# return render(request,'accounts/messagesend.html')

# me ="https://graph.facebook.com/v12.0/me?fields=id,name,first_name,last_name&access_token=EAACcfh61ZBs8BAHeYGjoIuymgqMOMxSROIQYqXQIfjySG6BhjkW1kAMZBFITNmrJRSgyjjuDwM9oU2o8KrBGEgokz1TRwqEIkxV20Wxpg68ARHABCqFr8WbC7OZAUn8uqRN95Vxhv6K3R3gy4tiENCZBhgpH1KqgKnlMFY60DAj17KQfAzUhlKCYnrwySmO7WKTrAC9ztl86c6UXZBx0K"
me = "https://graph.facebook.com/v12.0/me?fields=id,name,first_name,last_name&access_token=EAACUzJMgZCP8BACbe4QsQFDZACQzl1gVWvDZBQjJhLFETSkAeIOss5NonhRHzuxiBvuvZBTI16TO07NJoopZBSIVAktwZBRpos6sRLSu5wUbbtt4UT7YtBCUshxNPTdTFjNSePOcjn1WZBtZBZA1xpBzMD6WgTWo8DH5hBKN63ar1xfhOYoF4inHYZCb59u01PVG5XgRTxhGckltz0CYpSg8ZBp0I9gadGKvATuFw7lZCQQVdhXaMvvkMlZBZC"


# def get_facebook_data(me):
#     response = requests.get(me)
#     data = response.json()
#     return data

# url = "https://graph.facebook.com/v12.0/me?fields=id,name,first_name,last_name&access_token=EAACUzJMgZCP8BACbe4QsQFDZACQzl1gVWvDZBQjJhLFETSkAeIOss5NonhRHzuxiBvuvZBTI16TO07NJoopZBSIVAktwZBRpos6sRLSu5wUbbtt4UT7YtBCUshxNPTdTFjNSePOcjn1WZBtZBZA1xpBzMD6WgTWo8DH5hBKN63ar1xfhOYoF4inHYZCb59u01PVG5XgRTxhGckltz0CYpSg8ZBp0I9gadGKvATuFw7lZCQQVdhXaMvvkMlZBZC"

# response = requests.request("GET", url)
# data = response.json()
# return HttpResponse(data)

@login_required(login_url='login')
def bank_details(request):
    user = request.user
    name = request.POST.get('name')
    pan = request.POST.get('pan')
    gst = request.POST.get('gst')
    account_type = request.POST.get('account_type')
    bank_name = request.POST.get('bank_name')
    account_no = request.POST.get('account_no')
    account_no_ver = request.POST.get('account_no_ver')
    ifsc = request.POST.get('ifsc')
    swift = request.POST.get('swift_code')
    routing = request.POST.get('routing_code')

    data = BankDetail.objects.get(user_profile=user.profile)

    if request.method == "POST":
        details = BankDetail.objects.get(user_profile=user.profile)
        details.name = name
        details.pan_no = pan
        details.gst_no = gst
        details.account_type = account_type
        details.bank_name = bank_name
        details.account_no = account_no
        details.account_no_ver = account_no_ver
        details.ifsc_code = ifsc
        details.swift_code = swift
        details.routing_code = routing

        details.save()

        return HttpResponse('Saved')

    return render(request, 'accounts/bank_account_details.html', {'data': data})


@login_required(login_url='login')
def insta_temp(request):
    user = request.user
    userid = request.POST.get('username')
    if request.method == 'POST':
        data = Instagram_temp_data.objects.get(user_profile=user.profile)
        data.username = userid
        data.save()
        return redirect('dashboard_new')
    else:
        return redirect('dashboard_new')



def terms_conditions(request):
    return render(request, 'accounts/tnc.html') 