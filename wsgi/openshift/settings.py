#coding:utf-8

"""
Django settings for openshift project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import imp
import uuid
from datetime import datetime

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'ascq#%bii8(tld52#(^*ht@pzq%=nyb7fdv+@ok$u^iwb@2hwh'

default_keys = { 'SECRET_KEY': 'vm4rl5*ymb@2&d_(gc$gb-^twq9w(u69hi--%$5xrh!xk(t%hw' }
use_keys = default_keys
if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)


SECRET_KEY = use_keys['SECRET_KEY']

AUTH_USER_MODEL = 'userregistration.CustomUser'
# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
    DEBUG = True
else:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'contest',
    'article',
    'userregistration',
	'django_jenkins',
    'south',
    'sortedm2m',
    'execution',
    'changeemail',
    'teamsubmission',
    'clarification'
)
'''
if not ON_OPENSHIFT:
    print 'not on openshift'
    INSTALLED_APPS = ('debug_toolbar',) + INSTALLED_APPS
'''
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)


# If you want configure the REDISCLOUD
if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
    redis_server = os.environ['REDISCLOUD_URL']
    redis_port = os.environ['REDISCLOUD_PORT']
    redis_password = os.environ['REDISCLOUD_PASSWORD']
    CACHES = {
        'default' : {
            'BACKEND' : 'redis_cache.RedisCache',
            'LOCATION' : '%s:%d'%(redis_server,int(redis_port)),
            'OPTIONS' : {
                'DB':0,
                'PARSER_CLASS' : 'redis.connection.HiredisParser',
                'PASSWORD' : redis_password,
            }
        }
    }
    MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES + ('django.middleware.cache.FetchFromCacheMiddleware',)

ROOT_URLCONF = 'urls'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
     os.path.join(BASE_DIR,'templates'),
)



MYSQL = True
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if ON_OPENSHIFT:
    DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': os.environ['OPENSHIFT_APP_NAME'],
             'USER': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
             'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
             'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
             'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
             }
     }
elif MYSQL:
    DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'gentleidi',

			#'USER': os.environ['USER'],
             'USER': os.getenv('USER') or os.getenv('USERNAME'), #Added Windows support  
			 'PASSWORD': 'password',
			 'HOST': 'localhost',
			 'PORT': '3306',

         }
    }
else:
    DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         }
    }
    
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'
# Whether or not to use django's locale
USE_I18N = True
# Display dates, etc, as per local standard
USE_L10N = True
# Timezone-aware or not
USE_TZ = True

#DEBUG_TOOLBAR_PATCH_SETTINGS = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'
PRIVATE_MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'private')
PRIVATE_MEDIA_URL = '/private/'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATICFILES_DIRS = (
                    PROJECT_ROOT + '/static/',
                    )

# Fixture Directory

FIXTURE_DIRS = (
   PROJECT_ROOT + '/fixtures/',
)


def uploaded_filepath(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join('attachement', today, filename)

SUMMERNOTE_CONFIG = {
                     'attachment_upload_to': uploaded_filepath,
                     }
GRAPPELLI_ADMIN_TITLE = 'IDI Open'


ACCOUNT_ACTIVATION_DAYS = 7
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_USE_TLS = False
    EMAIL_HOST = 'smtp.idi.ntnu.no'
    EMAIL_PORT = 25
    DEFAULT_FROM_EMAIL = 'IDI Open <no-reply@idi.ntnu.no>'

