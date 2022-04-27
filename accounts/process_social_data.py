import json
from requests_oauthlib import OAuth1Session
import os
from django.conf import settings


def process_youtube_data(social_profile, data):
    try:
        items = data["items"][0]
        stats = items["statistics"]
        viewCount = int(stats["viewCount"])
        videoCount = int(stats["videoCount"])
        subscribers = int(stats["subscriberCount"])
        channel_id = items["id"]
        avgViews = round((viewCount / videoCount), 1)
        engagement_rate = round((subscribers / videoCount), 2)
        processed_data = {
            'social_profile': social_profile,
            'json_data': data,
            'videoCount': videoCount,
            'channel_id': channel_id,
            'viewCount': viewCount,
            'subscribers': subscribers,
            'engagement_rate': engagement_rate,
            'avgViews': avgViews
        }
    except:
        processed_data = {
            'social_profile': social_profile,
            'json_data': data,
            'videoCount': 0,
            'channel_id': None,
            'viewCount': 0,
            'subscribers': 0,
            'engagement_rate': 0,
            'avgViews': 0
        }
    return processed_data


def process_twitter_data(socialprofile, twitterprofile):
    data = twitterprofile.extra_data
    data_to_return = {
        "social_profile": socialprofile,
        "name": data["name"],
        "json_data": data,
        "username": data["screen_name"],
        "followers": data["followers_count"],
        "name": data["name"],
    }
    return data_to_return


def process_instagram_data(username, social_profile, json_data):
    # followers = json_data["edge_followed_by"]["count"]
    followers = json_data["follower"]
    likes = json_data
    comments = json_data
    engagement_rate = 0
    processed_data = {
        'username': username,
        'social_profile': social_profile,
        'json_data': json_data,
        'followers': followers,
        'likes': likes,
        'comments': comments,
        'engagement_rate': engagement_rate
    }
    return processed_data
