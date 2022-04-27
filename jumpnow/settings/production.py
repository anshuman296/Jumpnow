from .base import *

DEBUG = False

ALLOWED_HOSTS = ["139.59.57.121", "app.jumpnow.agency"]

try:
    with open(os.path.join(BASE_DIR, 'jumpnow/production.json')) as f:
        config_vars = json.load(f)
except:
    config_vars = None

db = config_vars['database']
email = config_vars['email']
rapidapi_key = config_vars['rapid_api_key']
twitter = config_vars['twitter']
youtube_api_key = config_vars['youtube_api_key']

FACEBOOK_TOKEN = config_vars['facebook_token']

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': db['name'],
    'USER': db['user'],
    'PASSWORD': db['password'],
    'HOST': db['host'],
    'PORT': db['port'],
  }
}


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


EMAIL_HOST_USER = email['email']
EMAIL_HOST_PASSWORD = email['password']

EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = 'smtp.privateemail.com'
EMAIL_USE_SSL = True
EMAIL_PORT = 465

EMAIL_VALIDATION = True

X_RAPID_API_KEY = rapidapi_key

GOOGLE_ANALYTICS_KEY = 'G-9L7QF0ESR2'

TWITTER_CONSUMER_KEY = twitter['consumer_keys']["api_key"]
TWITTER_CONSUMER_SECRET = twitter['consumer_keys']["api_secret_key"]
TWITTER_BEARER_TOKEN = twitter['bearer_token']
TWITTER_ACCESS_TOKEN = twitter['access']["token"]
TWITTER_ACCESS_SECRET = twitter['access']["secret"]

YOUTUBE_API_KEY = youtube_api_key