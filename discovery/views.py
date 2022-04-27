from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.conf import settings
import requests
import razorpay
import hmac
import hashlib
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from djqscsv import render_to_csv_response

# Custom Imports 
from discovery.models import *
from accounts.models import *
from dashboard.models import *
from accounts.decorators import subscribed_user, marketer
from accounts.forms import ContactForm, UserProfileForm
from discovery.forms import *

from algoliasearch_django import raw_search


@marketer
def discoveryMain(request):
    context = {
        'influencers': SocialMedia.objects.filter(featured=True)
    }
    return render(request, "discovery/discovery_landing.html", context)


def is_valid_queryparam(param):
    return param != '' and param is not None


@marketer
def search(request):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    campaignlists = campaignList.objects.filter(user=dp)
    context = {"campaignlists": campaignlists}
    return render(request, "discovery/search.html", context)


def subscriptions(request):
    return render(request, "discovery/subscriptions.html", context={})


def discovery_subscription_montly(request):
    sub_object = Subscription.objects.get(type="discovery", duration="1month")
    user = request.user
    profile = request.user.profile
    discovery_profile = DiscoveryProfile.objects.get(profile=profile)
    if discovery_profile.subscription is not None:
        messages.error(request, 'You are already subscribed')
        return redirect('discovery_search')
    res = requests.post("https://api.razorpay.com/v1/subscriptions",
                        auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET),
                        json={"plan_id": sub_object.razorpay_sub_id, "total_count": 12}
                        )
    return_data = res.json()
    return_data['user_data'] = {
        'name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        'contact': profile.mobile_number
    }
    return JsonResponse(return_data, status=res.status_code, safe=False)


def discovery_subscription_yearly(request):
    sub_object = Subscription.objects.get(type="discovery", duration="1year")
    user = request.user
    profile = request.user.profile
    discovery_profile = DiscoveryProfile.objects.get(profile=profile)
    if discovery_profile.subscription is not None:
        messages.error(request, 'You are already subscribed')
        return redirect('discovery_search')
    res = requests.post("https://api.razorpay.com/v1/subscriptions",
                        auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET),
                        json={"plan_id": sub_object.razorpay_sub_id, "total_count": 1})
    return_data = res.json()
    return_data['user_data'] = {
        'name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        'contact': profile.mobile_number
    }
    return JsonResponse(return_data, status=res.status_code, safe=False)


@csrf_exempt
def subscription_done_basic_monthly(request):
    sub_object = Subscription.objects.get(type="discovery", duration="1month")
    if request.method == 'POST':
        post_data = dict(request.POST)
        byte_key = (settings.RAZORPAY_SECRET).encode('UTF-8')
        plus_string = (f'{post_data["razorpay_payment_id"][0]}|{sub_object.razorpay_sub_id}')
        to_encode = plus_string.encode('UTF-8')
        h = hmac.new(byte_key, to_encode, hashlib.sha256).hexdigest()
        if not (settings.DEBUG):
            if h.upper() == post_data['razorpay_signature'][0].upper():
                messages.success(request, 'Thank you, you have successfully subscribed')
                profile = request.user.profile
                discovery_profile = DiscoveryProfile.objects.get(profile=profile)
                discovery_profile.searches_done = 0
                discovery_profile.subscription = sub_object
                discovery_profile.export_max = sub_object.exports
                discovery_profile.save()
                sub_finish_date = timezone.now() + timedelta(weeks=4)
                sub_payment = SubscriptionPayments.objects.create(
                    discovery_profile=discovery_profile,
                    subscription=sub_object,
                    payment_id=post_data["razorpay_payment_id"][0],
                    razorpay_subscription_id=post_data["razorpay_subscription_id"][0],
                    valid_till=sub_finish_date
                )
            else:
                messages.error(request, 'Some error occurred, please try again later!')
                print(h, post_data['razorpay_signature'])
        else:
            messages.success(request, 'Thank you, you have successfully subscribed')
            profile = request.user.profile
            discovery_profile = DiscoveryProfile.objects.get(profile=profile)
            discovery_profile.searches_done = 0
            discovery_profile.subscription = sub_object
            discovery_profile.export_max = sub_object.exports
            discovery_profile.save()
            sub_finish_date = timezone.now() + timedelta(weeks=4)
            sub_payment = SubscriptionPayments.objects.create(
                discovery_profile=discovery_profile,
                subscription=sub_object,
                payment_id=post_data["razorpay_payment_id"][0],
                razorpay_subscription_id=post_data["razorpay_subscription_id"][0],
                valid_till=sub_finish_date
            )
    return redirect('discovery_search')


@csrf_exempt
def subscription_done_basic_yearly(request):
    sub_object = Subscription.objects.get(type="discovery", duration="1year")
    if request.method == 'POST':
        post_data = dict(request.POST)
        bytes_secret = bytes(settings.RAZORPAY_SECRET, 'utf-8')
        to_encode = (f'{post_data["razorpay_payment_id"][0]}{sub_object.razorpay_sub_id}').encode()
        h = hmac.new(bytes_secret, to_encode, hashlib.sha256).hexdigest()
        if not (settings.DEBUG):
            if h.upper() == post_data['razorpay_signature'][0].upper():
                messages.success(request, 'Thank you, you have successfully subscribed')
                profile = request.user.profile
                discovery_profile = DiscoveryProfile.objects.get(profile=profile)
                discovery_profile.searches_done = 0
                discovery_profile.subscription = sub_object
                discovery_profile.export_max = sub_object.exports
                discovery_profile.save()
                sub_finish_date = timezone.now() + timedelta(weeks=52)
                sub_payment = SubscriptionPayments.objects.create(
                    discovery_profile=discovery_profile,
                    subscription=sub_object,
                    payment_id=post_data["razorpay_payment_id"][0],
                    razorpay_subscription_id=post_data["razorpay_subscription_id"][0],
                    valid_till=sub_finish_date
                )

            else:
                messages.error(request, 'Some error occurred, please try again later!')
                print(h, post_data['razorpay_signature'])
        else:
            messages.success(request, 'Thank you, you have successfully subscribed')
            profile = request.user.profile
            discovery_profile = DiscoveryProfile.objects.get(profile=profile)
            discovery_profile.searches_done = 0
            discovery_profile.subscription = sub_object
            discovery_profile.export_max = sub_object.exports
            discovery_profile.save()
            sub_finish_date = timezone.now() + timedelta(weeks=52)
            sub_payment = SubscriptionPayments.objects.create(
                discovery_profile=discovery_profile,
                subscription=sub_object,
                payment_id=post_data["razorpay_payment_id"][0],
                razorpay_subscription_id=post_data["razorpay_subscription_id"][0],
                valid_till=sub_finish_date
            )
    return redirect('discovery_search')


def discoveryInfluencerProfile(request, pk):
    influencer = SocialMedia.objects.get(id=pk)
    context = {"profile": influencer}
    return render(request, 'discovery/discovery_influencer_profile.html', context)
    # return render(request, 'discovery/show_influencers.html', context)


@subscribed_user
def campaignsMainPage(request):
    return render(request, 'discovery/campaign/all.html')


def show_user_details(request):
    # Twitter data
    print(request.user)
    tw_data = TwitterData.objects.get(social_profile=SocialMedia.objects.get(profile=request.user.profile))
    # Gets all the engagements to previous 10 posts
    print(tw_data.json_data)
    twitter_uid = tw_data.json_data["authtokens"]["id"]
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAIGNVAEAAAAAQpBgaGRJ4413hc9iSRA%2BdgHeVmc%3DakIKfNNRbE0Yrurb5H8sghaDqm5lzyYWXcFa9QS4mFZyEICANX"
    resp = requests.get(f'https://api.twitter.com/2/users/{twitter_uid}/followers',
                        headers={'Authorization': 'Bearer {}'.format(bearer_token)})

    resp_json = resp.json()
    followers = resp_json["meta"]["result_count"]
    print(followers)

    # Instagram data to be extracted
    tw_data = requests.get(f'https://facebook.graph.api/{ig_user_id}')

    # Facebook Data


@subscribed_user
def marketerProfile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    contact = Contact.objects.get(user_profile=user_profile)

    if request.method == 'POST':
        form_type = request.POST.get('submit')
        print(form_type)
        if form_type == 'profile-form-submitted':
            print("SAVING uform")
            uform = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            print(request.FILES)
            cform = ContactForm(initial=model_to_dict(contact))
            if uform.is_valid():
                uform.save()
                print("FORM saved")
                messages.success(request, 'Successfully updated profile data!')
            else:
                print(uform.errors)
        if form_type == 'contact-form-submitted':
            cform = ContactForm(request.POST, instance=contact)
            uform = UserProfileForm(initial=model_to_dict(user_profile))
            if cform.is_valid():
                cform.save()
                messages.success(request, 'Successfully updated contact data!')
            else:
                print(cform.errors)
    else:
        cform = ContactForm(initial=model_to_dict(contact))
        uform = UserProfileForm(initial=model_to_dict(user_profile))

    context = {
        'uform': uform,
        'cform': cform,
        'userimage': user_profile.profile_image,
        'bill_date': user_profile.discovery.get().payments.get().valid_till
    }

    return render(request, 'discovery/marketer_profile.html', context)


@subscribed_user
def getCampaigns(request):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    camps = Campaign.objects.filter(user=dp)
    qs_json = serializers.serialize('json', camps)
    return HttpResponse(qs_json, content_type='application/json')


@subscribed_user
def getCampaignLists(request, id):
    campaign = Campaign.objects.get(id=id)
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    if request.user == dp.profile.user:
        lists = campaignList.objects.filter(campaign=campaign)
        qs_json = serializers.serialize('json', lists)
        return HttpResponse(qs_json, content_type='application/json')
    else:
        return HttpResponse("Not Authorized", status=403)


@subscribed_user
def addToCampaignLists(request):
    if request.method == 'POST':
        user = request.user
        dp = DiscoveryProfile.objects.get(profile=user.profile)
        print(request.POST)
        # assigned_campaigns = AssignedCampaign.objects.all()
        list_profiles = request.POST.get('profiles', False)
        # list_profiles = list_profiles.split(',')
        campaign_name_existing = request.POST.get('blank1', False)
        campaign_name_new = request.POST.get('campaign_name', False)
        campaign_list_name_existing = request.POST.get('campaign_list', False)
        campaign_list_name_new = request.POST.get('blank2', False)

        if campaign_name_existing and (campaign_name_existing != 'new3-campaign'):
            campaign = Campaign.objects.get(id=int(campaign_name_existing))
            if campaign_list_name_existing and (campaign_list_name_existing != 'new3-campaign-list'):
                campaign_list = campaignList.objects.get(id=int(campaign_list_name_existing))
                old_profiles = campaign_list.profiles.all()
                old_p_list = []
                for old_p in old_profiles:
                    old_p_list.append(old_p.id)
                for p in list_profiles:
                    if int(p) not in old_p_list:
                        profile = SocialMedia.objects.get(id=int(p))
                        campaign_list.profiles.add(profile)
                campaign_list.save()
            elif (campaign_list_name_new):
                campaign_list = campaignList.objects.create(name=campaign_list_name_new, campaign=campaign)
                for p in list_profiles:
                    profile = SocialMedia.objects.get(id=int(p))
                    campaign_list.profiles.add(profile)
        elif campaign_name_new:
            campaign = Campaign.objects.create(campaign_name=campaign_name_new,
                                               user=dp)

            campaign.save()

        return HttpResponse('Success', status=200)


@subscribed_user
def discoveryCampaignsMain(request):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    camps = Campaign.objects.filter(user=dp)
    context = {'cps': camps}
    return render(request, 'discovery/campaignMain.html', context)


@subscribed_user
def discoveryCampaignSingle(request, pk):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    camp = Campaign.objects.get(id=pk)
    cp_lists = campaignList.objects.filter(campaign=camp)
    context = {'lists': cp_lists, 'cp': camp}
    # return render(request, 'discovery/campaignSingle.html', context)
    return render(request, 'discovery/show.html', context)


@subscribed_user
def campaignListSingle(request, pk):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    cp_list = campaignList.objects.get(id=pk)
    context = {'list': cp_list}
    return render(request, 'discovery/listSingle.html', context)


@subscribed_user
def exportInfluencerList(request):
    if request.method == 'POST':
        disocvery_profile = DiscoveryProfile.objects.get(profile=request.user.profile)
        if disocvery_profile.exports_done < disocvery_profile.subscription.exports:
            inf_list = request.POST.getlist('profiles[]')
            inf_objects = SocialMedia.objects.filter(id__in=inf_list).values(
                'jumpnow_score',
                'profile__business_email',
                'profile__user__first_name',
                'profile__user__last_name',
                'profile__bio',
                'profile__gender'
            )
            return render_to_csv_response(inf_objects)
        else:
            return JsonResponse({'status': 'Max number of exports reached'}, status=403)
    return HttpResponse('Success', status=200)


# @subscribed_user
def CreatorDiscoveryProfile(request, id):
    social_profile = SocialMedia.objects.get(id=id)
    context = {'profile': social_profile}

    return render(request, 'discovery/creator_discovery_profile.html', context)


@DiscoveryProfile
def show_influencer(request):
    influencer = SocialMedia.objects.all()
    context = {"profile": influencer}
    return render(request, 'discovery/show_influencers.html', context)


@DiscoveryProfile
def show_profiles(request):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    profiles = SocialMedia.objects.all()
    campaign_list = campaignList.objects.all()
    context = {'profiles': profiles, 'campaign_list': campaign_list}
    return render(request, 'discovery/show_profile.html', context)


@marketer
def Addcampaign(request):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)

    campaign_name_new = request.POST.get('campaign_name', False)
    campaign_description = request.POST.get('campaign_description', False)
    campaign_bidding = request.POST.get('bidding', False)
    list_profiles = request.POST.getlist('campaign_list', False)

    if request.method == 'POST':
        if campaign_bidding == 'on':
            campaign_bidding = True
        else:
            campaign_bidding = False
        campaign = Campaign.objects.create(campaign_name=campaign_name_new, campaign_description=campaign_description,
                                           user=dp, bidding=campaign_bidding)
        assign_id = campaign.id
        if list_profiles:
            for p in list_profiles:
                profile = campaignList.objects.get(id=int(p))
                campaign.campaign_list.add(profile)
                user_profiles = profile.profiles.all()
                for user_profile in user_profiles:
                    assign_creator = AssignedCreators.objects.create(user_profile=user_profile.profile)
                    assign_creator.save()
                    campaign.assigned_creators.add(assign_creator.id)

            campaign.save()
    form = CampaignForm()
    # return render(request, 'discovery/list_main.html', {'form': form})
    return render(request, 'discovery/add_campaign.html', {'form': form})


@marketer
def add_deliverable(request, id):
    user = request.user
    platform = request.POST.get('platform')
    deliverable = request.POST.get('type')
    assigned_creator = AssignedCreators.objects.get(id=id)
    if request.method == 'POST':
        assigned_creator.deliverables.create(user_profile=user.profile, platform=platform, deliverable=deliverable)
        assigned_creator.save()
        return HttpResponse('Added Succesfully')
    
    assigned_creator = AssignedCreators.objects.get(id=id)
    deliverable = assigned_creator.deliverables.all()
    return render(request, 'discovery/delivarables.html',{'deliverable': deliverable,
                                                                'assigned_creator': assigned_creator})


@marketer
def Addcampaignlist(request):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    list_profiles = request.POST.getlist('profiles', False)
    campaign_list_name_new = request.POST.get('list_name', False)
    platform = request.POST.get('platform', False)

    if request.method == 'POST':
        campaign_list = campaignList.objects.create(list_name=campaign_list_name_new, platform=platform, user=dp)
        if list_profiles:
            for p in list_profiles:
                profile = SocialMedia.objects.get(id=int(p))
                campaign_list.profiles.add(profile)
            campaign_list.save()

    form = CampaignListForm()

    # return render(request, 'discovery/list_main.html', {'form': form})
    # return render(request, 'discovery/search.html', {'form': form})
    return redirect(showcampaignlists)


@marketer
def showcampaigns(request):
    user = request.user
    dp = DiscoveryProfile.objects.get(profile=user.profile)
    campaign = Campaign.objects.filter(user=dp)
    context = {'campaigns': campaign}
    return render(request, 'discovery/show_campaigns.html', context)


@marketer
def showcampaignlists(request):
    # user = request.user
    dp = DiscoveryProfile.objects.get(profile=request.user.profile)
    campaignlists = campaignList.objects.filter(user=dp)
    campaign_list = {'campaignlists': campaignlists}
    return render(request, 'discovery/list_main.html', campaign_list)
    # return render(request, 'discovery/search_base.html', campaign_list)


@marketer
def addinfluencertolist(request, id):
    dp = DiscoveryProfile.objects.get(profile=request.user.profile)
    campaignlists = campaignList.objects.filter(user=dp)
    if request.method == 'POST':
        list_id = request.POST.get('list_id', False)
        camp_list = campaignList.objects.get(id=list_id)
        camp_list_profiles = camp_list.profiles.all()
        profile = SocialMedia.objects.get(id=id)
        if profile in camp_list_profiles:
            messages.info(request, "Profile already in list")
            print('Profile already in list')
        else:
            camp_list.profiles.add(id)
            camp_list.save()
            print('Profile added succesfully')
            return redirect('discovery_search')
    context = {'campaignlists': campaignlists}
    return render(request, 'discovery/add_influencer_to_list.html', context)
    # return render(request,'discovery/search.html',context)

@marketer
def removeinfluencerfromlist(request, id, list_id):
    campaignlist = campaignList.objects.get(id=list_id)
    campaignlist.profiles.remove(id)
    campaignlist.save()
    return redirect(showcampaignlists)


@marketer
def viewinfluencerlist(request, id):
    campaignlists = campaignList.objects.get(id=id)
    context = {'campaignlists': campaignlists}
    return render(request, 'discovery/view_influencers_list.html', context)


@marketer
def allinfluencerslist(request):
    influencers_list = SocialMedia.objects.all()
    return render(request, 'discovery/all_influencers_list.html', {'influencers_list': influencers_list})

@marketer
def campaign_creators(request, id):
    context = {}
    context['campaign'] = Campaign.objects.get(id=id)
    context['creators'] = context['campaign'].assigned_creators.all()
    return render(request, 'discovery/campaign_creators.html', context)

@marketer
def creator_details(request, id):
    assigned_creator = AssignedCreators.objects.get(id=id)
    return print('hello')

@marketer
def assigned_details(request, id):
    context = {}
    context['creator'] = AssignedCreators.objects.get(id=id)
    context['campaign'] = Campaign.objects.get(assigned_creators=id)

    return render(request, 'discovery/assigned_details.html', context)

@marketer
def view_deliverables(request, id):
    assigned_creator = AssignedCreators.objects.get(id=id)
    deliverable = assigned_creator.deliverables.all()
    return render(request, 'discovery/view_deliverables.html', {'deliverable': deliverable,
                                                                'assigned_creator': assigned_creator})

@marketer
def content_review(request, id):
    deliverable = Deliverables.objects.get(id=id)
    return render(request, 'discovery/content_review.html', {'deliverable': deliverable})


@marketer
def accept_review(request, id):
    if request.method == 'POST':
        remark = request.POST.get('remark', False)
        deliverable = Deliverables.objects.get(id=id)
        deliverable.remark = remark
        deliverable.review_accepted = True
        deliverable.save()
    return HttpResponse('Content accepted')



# @subscribed_user
# def addinfluencertolist(request,id):
#     if request.method == 'POST':
#         lists = request.POST.getlist('listassign', False)
#         print('listttt',lists)
#         for i in lists:
#             print('iii',i)
#         #     camp_list = campaignList.objects.get(id = id)
#         # if comp_object:
#         #     # com_list = Campaign.objects.filter(campaign_list__in=lists)
#         #     for i in lists:
#         #         # instance = Campaign.objects.get(id=id)
#         #         comp_object.campaign_list.add(i)
#     return HttpResponse('Influencer Added to list!!!')
@marketer
def algolia_search(request):
    response = raw_search(InstagramData, "delhi")
    return JsonResponse({"response": response})



me = "https://graph.facebook.com/v11.0/me?fields=birthday&access_token=EAACcfh61ZBs8BAHeYGjoIuymgqMOMxSROIQYqXQIfjySG6BhjkW1kAMZBFITNmrJRSgyjjuDwM9oU2o8KrBGEgokz1TRwqEIkxV20Wxpg68ARHABCqFr8WbC7OZAUn8uqRN95Vxhv6K3R3gy4tiENCZBhgpH1KqgKnlMFY60DAj17KQfAzUhlKCYnrwySmO7WKTrAC9ztl86c6UXZBx0K"

# def get_facebook_data(me):
#     response = requests.get(me)
#     data = response.json()
#     return data
