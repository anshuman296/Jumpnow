from django.dispatch.dispatcher import receiver
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from discovery.models import DiscoveryProfile, UserProfile
from allauth.socialaccount.signals import social_account_added


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard_new')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                groups = request.user.groups.all()

            for group in groups:
                if group.name in allowed_roles:
                    return view_func(request, *args, **kwargs)

            return HttpResponse("Not Allowed", status=403)

        return wrapper

    return decorator


def subscribed_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            discovery_profile = DiscoveryProfile.objects.get(profile=request.user.profile)
            if discovery_profile.subscription:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('discovery_search')
        else:
            return redirect('index')

    return wrapper


def marketer(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            discovery_profile = DiscoveryProfile.objects.get(profile=request.user.profile)
            if discovery_profile:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('discovery_search')
        else:
            return redirect('index')

    return wrapper


def creator(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            creator_profile = UserProfile.objects.get(user=request.user)
            if creator_profile.creator:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('dashboard_new')
        else:
            return redirect('index')
    return wrapper


def complete_profile(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.complete:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('social_connect')
        else:
            return redirect('index')

    return wrapper
