import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing


if 'main' in os.getcwd():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.production')
elif 'qa' in os.getcwd():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.qa')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.dev')


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})