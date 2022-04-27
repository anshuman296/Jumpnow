from accounts.models import InstagramData, SocialMedia, UserProfile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import pandas as pd
import os
from pathlib import Path
import requests
from django.conf import settings
import time
from tqdm import tqdm
from io import BytesIO
from django.core import files
import random

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR_PARENT = Path(__file__).resolve().parent.parent.parent.parent

data = pd.read_csv(os.path.join(BASE_DIR_PARENT, 'data\ig_influencers.csv'))

def divide_fullname_into_first_and_last(name):
    if name:
        name_list = name.split(' ')
        if len(name_list) > 1:
            first_name = name_list[0]
            name_list.remove(first_name)
            last_name = ' '.join(name_list)
        else:
            first_name = name
            last_name = None
        return first_name, last_name


def save_profile_picture(image_url):
    url = image_url
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        #  Error handling here
        return False

    fp = BytesIO()
    fp.write(resp.content)
    file_name = url.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
    return file_name, files.File(fp)
    

def create_user(username, full_name):
    username = username
    first_name, last_name = divide_fullname_into_first_and_last(full_name)
    if first_name and last_name:
        return User.objects.get_or_create(first_name=first_name, last_name=last_name, username=username, is_active=False)
    else:
        return User.objects.get_or_create(first_name=first_name, username=username, is_active=False)

def create_user_profile(user):
    return UserProfile.objects.get_or_create(user=user, registered=False, complete=False, creator=True)

def create_social_media_profile(profile):
    sm, created = SocialMedia.objects.get_or_create(profile=profile, connected_profiles=['instagram'])
    sm.tags.add('instagram')
    sm.save()
    return  sm, created

def get_data_from_api(username, profile):
    headers = {
        'x-rapidapi-key': settings.X_RAPID_API_KEY_INSTAGRAM_KEY,
        'x-rapidapi-host': settings.X_RAPID_API_KEY_INSTAGRAM_HOST
    }
    url = f'{settings.X_RAPID_API_KEY_INSTAGRAM_ENDPOINTS["accounts"]}/{username.strip()}/info'
    response = requests.request("GET", url, headers=headers)
    data = response.json()['data']
    if response.status_code != requests.codes.ok:
        #  Error handling here
        print(response.status_code)
        return False, False
    return {
        'social_profile': profile,
        'json_data': response.json()['data'],
        'instagram_id': data['id'],
        'username': data['username'],
        'full_name': data['full_name'],
        'bio': data['biography'],
        'posts': data['figures']['posts'],
        'followers': data['figures']['followers'],
        'followings': data['figures']['followings'],
        'is_verified': data['is_verified'],
        'category': data['business']['category']
    }, data['profile_picture']['hd'] or data['profile_picture']['normal']

def create_instagram_profile(profile, username):
    user_data, image_url = get_data_from_api(username, profile)
    if user_data:
        ig_user = InstagramData.objects.create(**user_data)
        filename, file = save_profile_picture(image_url)
        ig_user.profile_image.save(f'{ig_user.instagram_id}.jpg', file)
        return ig_user
    return False
class Command(BaseCommand):
    help = 'Creates instagram users based on username'

    def handle(self, *args, **options):
        for row in tqdm(data.itertuples()):
            user, created = create_user(row[2], row[1])
            profile, created = create_user_profile(user)
            social_media_profile, created = create_social_media_profile(profile)
            try:
                instagram_profile = create_instagram_profile(social_media_profile, user.username)
            except Exception as e:
                print(e)
            time.sleep(random.randint(7, 15))