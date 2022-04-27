import os

from django.core.wsgi import get_wsgi_application

if 'main' in os.getcwd():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.production')
elif 'qa' in os.getcwd():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.qa')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.dev')  

application = get_wsgi_application()