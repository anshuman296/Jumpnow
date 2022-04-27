from http.client import responses
import requests
from django.conf import settings
from TikTokApi import TikTokApi
import tweepy
import json
from googleapiclient.discovery import build
import facebook
import google.oauth2.credentials
import google_auth_oauthlib.flow
from accounts.models import YoutubeAuth
from django.forms.models import model_to_dict





auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET)

twitter_api = tweepy.API(auth)


# def get_instagram_userid(username):
#     url = "https://instagram85.p.rapidapi.com/account/username/info"
#
#     headers = {
#         'x-rapidapi-key': "7d81862b91msh701204cf56b7b14p13ead0jsndf392595d6d6",
#         'x-rapidapi-host': "instagram85.p.rapidapi.com"
#     }
#     response = requests.request("GET", url, headers=headers)
#     data = response.json()
#     return data

def get_instagram_userid(username):
    url = "https://easy-instagram-service.p.rapidapi.com/username"

    querystring = {"username": username}

    headers = {
        'x-rapidapi-host': "easy-instagram-service.p.rapidapi.com",
        'x-rapidapi-key': "7d81862b91msh701204cf56b7b14p13ead0jsndf392595d6d6"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data =response.json()
    return data



def get_twitter_data(username):
    url = "https://twitter32.p.rapidapi.com/getProfile"

    querystring = {"username": username}

    headers = {
        'x-rapidapi-host': "twitter32.p.rapidapi.com",
        'x-rapidapi-key': "7d81862b91msh701204cf56b7b14p13ead0jsndf392595d6d6"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


def get_youtube_data(user):
    credentials = YoutubeAuth.objects.get(user_id=user)
    credentials = model_to_dict(credentials, exclude=['id', 'user_id'])
    youtube_api = build('youtube', 'v3', credentials=google.oauth2.credentials.Credentials(**credentials))
    response = youtube_api.channels().list(part='statistics, id', mine=True).execute()
    return response



# def get_facebook_data(username):
#     print("In social api facebook")
#     post = fb_graph.get_connections(id='me',connection_name="friends")
#
#     print(post)
#     return post

# def get_facebook_data(me):
#     response = requests.get(me)
#     data = response.json()
#     return data

