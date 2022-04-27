from django.shortcuts import render

# Create your views here.

def privacy_policy(request):

    return render(request, 'extras/privacy-policy.html')

def tnc(request):
    return render (request, 'extras/tnc.html')

    