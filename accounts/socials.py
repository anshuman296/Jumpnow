from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse
from post_office import mail
from django.conf import settings
import json

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def authentication_error(self, request, provider_id, error, exception, extra_context):
        # your_log_function(
        #     'SocialAccount authentication error!',
        #     'error',
        #     request,
        # )
        pass
        # extra_data = {'provider_id': provider_id, 'error': error.__str__(), 'exception': exception.__str__(), 'extra_context': extra_context}
        
        
        # print(extra_data)
        # mail.send(
        #     ['ishant@jumpnow.agency'],
        #     subject = "Social Account Error Notify",
        #     sender = settings.EMAIL_HOST_USER,
        #     message = json.dumps(extra_data),
        #     priority='now',
        # )
        # return HttpResponse(extra_data, status=500)