from slack import WebClient
from slack.errors import SlackApiError
from django.conf import settings

slack_token = settings.SLACK_BOT_TOKEN
client = WebClient(token=slack_token)

def send_celebrity_sign_up_notification(influencer):
    message = f"Hey Admin, a potential celebrity has signed up. Please visit {settings.URL_BACKEND}/admin/accounts/socialmedia/{influencer.id}/change/ to verify his application. Thanks!"
    try:
        response = client.chat_postMessage(
            channel = 'C01THLDRR53',
            text=message
        )
    except SlackApiError as e:
        print(e)
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'