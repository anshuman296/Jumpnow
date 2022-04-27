from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect



# Create your views here.

def jumpnow_main(request):
    return render(request, 'main/landingPage_2.html')



def tnc(request):
    return render(request,'main/tnc.html')

def privacy(request):
    return render(request,'main/privacy_notice.html')

def redirect_fun(request):
    return redirect('index')

def contactUs(request):
    return render(request,'main/contact_us.html')

def aboutJN(request):
    return render(request,'main/about.html')