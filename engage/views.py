from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from datetime import datetime, time
from django.contrib import messages
from datetime import datetime, timedelta
from django.conf import settings
import requests
import razorpay
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt

from engage.forms import NewGigForm, NewDOForm, NewDisputeForm
from engage.models import DirectOffer, Gig, GigPaymentID, JobCreationCharges
from engage.notify_signals import *
from chat.models import ChatMessage, ChatGroup

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))

def gigs_main(request):
    gigs = Gig.objects.filter(marketer_id=request.user) 
    context = {
        "gigs": gigs,
        "total_gigs": gigs.count(),
        "active_gigs": gigs.filter(start_date_bid__gte=datetime.now(), end_date_bid__lte=datetime.now()).count(),
        "bid_on_active_projects": 5
        }
    return render(request, 'engage/gigs-main.html', context)

def create_gig(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        data = {
            "marketer_id": request.user,
            "name": request.POST.get("gigname"),
            "description": request.POST.get("description"),
            "budget": request.POST.get("budget"),
            "open_for_bidding": True if request.POST.get("bid-check")=='on' else False,
            "platforms": request.POST.getlist("platforms[]"),
        }
        if data["open_for_bidding"]:
            data["start_date_bid"] = datetime.strptime(f'{request.POST.get("bid-start-date")} {request.POST.get("bid-start-time")}:00', '%d-%m-%Y %H:%M:%S')
            data["end_date_bid"] = datetime.strptime(f'{request.POST.get("bid-end-date")} {request.POST.get("bid-end-time")}:00', '%d-%m-%Y %H:%M:%S')
            
            
        new_gig = Gig.objects.create(**data)
        messages.success(request, f'New Gig Successfully created!')
        return redirect('gigs-main')

    return render(request, 'engage/create_gig.html', context)


def create_direct_offer(request):
    context = {}
    form = NewDOForm()
      
    if request.method == 'POST':
        data = {
            'gig_id': Gig.objects.get(id=request.POST.get("gig_id")),
            'creator': User.objects.get(id=request.POST.get("creator")),
            'amount': int(request.POST.get("amount")),
            "expires": datetime.now() + timedelta(days=int(request.POST.get("expires_in")))
        }
        print(data)
        do = DirectOffer.objects.create(**data)

        messages.success(request, "Successfully send direct offer!")
        send_direct_offer_notification(request.user, do)
        return redirect('gigs-main')
  
    context['form']= form

    return render(request, 'engage/create_direct_offer.html', context)

def raise_dispute(request):
    context = {}
    form = NewDisputeForm(request.POST or None, request.FILES or None)
      
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()
  
    context['form']= form

    return render(request, 'engage/raise_dispute.html', context)

def create_gig_payment_object(request, gig_id):
    gig = Gig.objects.get(id=gig_id)
    charges = JobCreationCharges.objects.first()
    user = request.user
    profile = request.user.profile
    amount_in_rupees = (gig.budget + ((charges.gig_extra/100)*gig.budget))
    final_amount = amount_in_rupees*100
    gig.final_amount = amount_in_rupees
    gig.save()
    notes = {'New Gig': f'User - {gig.marketer_id.first_name}'}
    res = requests.post("https://api.razorpay.com/v1/orders",
    auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET),
    json={ "amount": final_amount, "currency": 'INR', "notes": notes })
    return_data = res.json()
    return_data['user_data'] = {
        'name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        'contact': profile.mobile_number
    }
    print(return_data)
    return JsonResponse({'status': 'success', 'url': 'asdfawe', 'data': return_data}, status=200)

@csrf_exempt
def gig_payment_done(request):
    if request.method == 'POST':
        params_dict = {
            'razorpay_order_id': request.POST.get('razorpay_order_id'),
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_signature': request.POST.get('razorpay_signature')
        }
        rp = razorpay_client.utility.verify_payment_signature(params_dict)
        gig = Gig.objects.get(id=request.POST.get('gig_id', False))
        gig_payment = GigPaymentID.objects.create(
            payment_id=params_dict["razorpay_payment_id"],
            order_id=params_dict["razorpay_order_id"],
            signature=params_dict["razorpay_signature"],
            payment_amount=gig.final_amount
        )
        gig.paid_for = True
        gig.payment_id = gig_payment
        gig.save()
        print("LOLL")
    messages.success(request, 'congratulations!')
    return JsonResponse({'status': 'success'}, status=200)

@csrf_exempt
def send_payment_to_influencer(request, gig_id):
    gig = Gig.objects.get(id=gig_id)
    res = requests.post("https://api.razorpay.com/v1/orders",
    auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET),
    json={ "amount": gig.budget,
          "currency": 'INR', 
            "payment_capture": 1,
            "transfers": [
                {
                    "account": "acc_HSWYjiNn89OJF7",
                    "amount": gig.budget,
                    "currency": 'INR',
                    "on_hold": True,
                }
            ]
           })
    print(res.json())
    return JsonResponse({'status': 'success'})