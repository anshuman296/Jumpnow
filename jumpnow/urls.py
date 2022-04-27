from django.contrib import admin
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from accounts.views import social_login_cancelled
from dashboard.views import main as social_account_profile
import notifications.urls


# jumpnow.agency/discovery/search/

urlpatterns = [
    path('admin/', admin.site.urls),
    path('discovery/', include('discovery.urls')),
    path('', include('dashboard.urls')),
    path('engage/chat/', include('chat.urls')),
    path('engage/', include('engage.urls')),
    path('', include('accounts.urls')),
    path('', include('extras.urls')),
    path('home/',include('main.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    url(r'^accounts/social/login/cancelled/$', social_login_cancelled),
    url(r'^accounts/profile/$', social_account_profile),
    path('accounts/', include('allauth.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('payment/',include('payments.urls'))

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)