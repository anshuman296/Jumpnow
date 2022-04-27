from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from jumpnow.settings.dev import RAZORPAY_ID, RAZORPAY_SECRET
from discovery.models import AssignedCreators
import requests

# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
#     auth=(RAZORPAY_ID, RAZORPAY_SECRET)
#     )
#
#
# def homepage(request):
#     currency = 'INR'
#     amount = 200*100  # Rs. 200
#
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
#
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
#
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = RAZORPAY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
#
#     return render(request, 'index.html', context=context)
#
#
# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
# @csrf_exempt
# def paymenthandler(request):
#
#     # only accept POST request.
#     if request.method == "POST":
#         try:
#
#             # get the required parameters from post request.
#             print("In post try")
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#             print(params_dict)
#
#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             print(result)
#             if result is None:
#                 amount = 20000  # Rs. 200
#                 try:
#
#                     # capture the payemt
#
#                     razorpay_client.payment.capture(payment_id, amount)
#                     print(payment_id)
#
#                     body = {
#                     "transfers": [
#                         {
#                             "account": "acc_id",
#                             "amount": 0.15*amount,
#                             "currency": "INR",
#                             "notes": {
#                                 "name": "Gaurav Kumar",
#                                 "roll_no": "IEC2011025"
#                             },
#                             "linked_account_notes": [
#                                 "roll_no"
#                             ],
#                             "on_hold": True,
#                             "on_hold_until": 1671222870
#                         },
#                         {
#                             "account": "acc_id",
#                             "amount": 100,
#                             "currency": "INR",
#                             "notes": {
#                                 "name": "Saurav Kumar",
#                                 "roll_no": "IEC2011026"
#                             },
#                             "linked_account_notes": [
#                                 "roll_no"
#                             ],
#                             "on_hold": False
#                         }
#                     ]
#                 }
#
#
#                     # render success page on successful caputre of payment
#
#                     create_transfer = requests.post(f'https://api.razorpay.com/v1/payments/{payment_id}/transfers',
#                     data=body,auth=(RAZORPAY_ID, RAZORPAY_SECRET))
#
#                     return render(request, 'paymentsuccess.html')
#                 except:
#
#                     # if there is an error while capturing payment.
#                     return render(request, 'paymentfail.html')
#             else:
#
#                 # if signature verification fails.
#                 return render(request, 'paymentfail.html')
#         except:
#
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(RAZORPAY_ID, RAZORPAY_SECRET)
)


def pay(request, id):
    creator = AssignedCreators.objects.get(id=id)
    amount = creator.settled_amount * 100
    currency = 'INR'
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0',
                                                       ))

    razorpay_order_id = razorpay_order['id']

    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = "rzp_test_dJZ7Ag8fecq3wT"
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['creator_id']= creator.id

    return render(request, 'index.html', context=context)


@csrf_exempt
def paymenthandler(request, id):
    creator = AssignedCreators.objects.get(id = id)
    amount = creator.settled_amount * 100
    if request.method == "POST":
        try:

            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            print(razorpay_order_id, payment_id, signature)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is None:
                amount = amount
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    creator.payment = True
                    creator.rzrpay_order_id = razorpay_order_id
                    creator.rzrpay_payment_id = payment_id
                    creator.save()
                    return render(request, 'success.html')
                except:
                    return render(request, 'paymentfail.html')




        except:
            return HttpResponseBadRequest(" cannot capture")
    else:
        return HttpResponseBadRequest('Not a post request')
