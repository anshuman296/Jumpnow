from django.conf import settings

def gtag(request):
    return {
        "GOOGLE_ANALYTICS_KEY": settings.GOOGLE_ANALYTICS_KEY,
    }

def notifications(request):
    if request.user.is_authenticated:
        return {
            "notifications": request.user.notifications.unread(),
        }
    else:
        return {
            "notifications": [],
        }

