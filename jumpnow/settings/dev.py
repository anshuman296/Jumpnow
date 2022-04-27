from .base import *

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0",
                 "65.2.152.193", "devapp.jumpnow.agency",
                 "3.109.146.108","app.jumpnow.agency",
                 "jumpnow.agency",
                 "127.0.0.1", "localhost"]

try:
    # with open(os.path.join(STATIC_ROOT, 'cred/json/dev.json')) as f:
    with open(os.path.join(BASE_DIR, 'jumpnow/dev.json')) as f:



    # # with open(os.path.join(STATIC_ROOT, 'cred/json/dev.json')) as f:
    # with open(os.path.join(BASE_DIR, 'jumpnow/dev.json')) as f:

        config_vars = json.load(f)
except:
    config_vars = None

db = config_vars['database']
email = config_vars['email']
rapidapi_key = config_vars['rapid_api_key']
rapidapi_key_new = config_vars["rapid_api"]
twitter = config_vars['twitter']
youtube_api_key = config_vars['youtube_api_key']
facebook = config_vars['facebook']
razorpay = config_vars['razorpay']
slack = config_vars['slack']
sentry = config_vars['sentry']
# GOOGLE_CRED_FILE = config_vars['google_cred_file']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = (os.path.join(STATIC_ROOT, 'cred/json/client_secret.json'))
GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = (os.path.join(BASE_DIR, 'jumpnow/client_secret.json'))



if sentry:
    sentry_sdk.init(
        dsn="https://32bf6e72522043ea978532538e016811@o987026.ingest.sentry.io/5943816",
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

URL_BACKEND = config_vars['backend_url']
SLACK_USER_TOKEN = slack["user_oauth_token"]
SLACK_BOT_TOKEN = slack["bot_user_oauth_token"]
FACEBOOK_TOKEN = facebook['token']


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

TORTOISE_INIT = {
    "db_url": f"postgres://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}",
    "modules" : {
        "models": ["chat.tortoise_models", "aerich.models"],
        "default_connection": "default",
     }
}


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


EMAIL_HOST_USER = email['email']
EMAIL_HOST_PASSWORD = email['password']

EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_USE_SSL = True
EMAIL_PORT = 465

DEFAULT_FROM_EMAIL = email['email']

EMAIL_VALIDATION = False

POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now',
}

X_RAPID_API_KEY = rapidapi_key

X_RAPID_API_KEY_NEW = rapidapi_key_new
X_RAPID_API_KEY_INSTAGRAM_KEY = rapidapi_key_new["instagram"]["X-RapidAPI-KEY"]
X_RAPID_API_KEY_INSTAGRAM_HOST = rapidapi_key_new["instagram"]["X-RapidAPI-HOST"]
X_RAPID_API_KEY_INSTAGRAM_ENDPOINTS = rapidapi_key_new["instagram"]["endpoints"]


GOOGLE_ANALYTICS_KEY = ''

TWITTER_CONSUMER_KEY = twitter['consumer_keys']["api_key"]
TWITTER_CONSUMER_SECRET = twitter['consumer_keys']["api_secret_key"]
TWITTER_BEARER_TOKEN = twitter['bearer_token']
TWITTER_ACCESS_TOKEN = twitter['access']["token"]
TWITTER_ACCESS_SECRET = twitter['access']["secret"]

RAZORPAY_ID = razorpay['id']
RAZORPAY_SECRET = razorpay['secret']

SOCIAL_AUTH_FACEBOOK_KEY = facebook['app_id']
SOCIAL_AUTH_FACEBOOK_SECRET = facebook['app_secret']



YOUTUBE_API_KEY = youtube_api_key

SOCIALACCOUNT_ADAPTER = "accounts.socials.SocialAccountAdapter"

ACCOUNT_SIGNUP_REDIRECT_URL = '/register/creator/connect_accounts'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v10.0',
    }
}

