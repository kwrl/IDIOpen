#coding:utf-8
BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "amqp"
import subprocess

CELERYD_NODES = "w1"
CELERY_MULTI = "celery multi"


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

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'ascq#%bii8(tld52#(^*ht@pzq%=nyb7fdv+@ok$u^iwb@2hwh'

default_keys = { 'SECRET_KEY': 'vm4rl5*ymb@2&d_(gc$gb-^twq9w(u69hi--%$5xrh!xk(t%hw' }
use_keys = default_keys

SECRET_KEY = use_keys['SECRET_KEY']

AUTH_USER_MODEL = 'userregistration.CustomUser'
# SECURITY WARNING: don't run with debug turned on in production!
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
    #'debug_toolbar',
    'openshift.contest',
    'openshift.article',
    'openshift.userregistration',
	'django_jenkins',
    'south',
    'sortedm2m',
    'openshift.changeemail',
    'openshift.execution',
    'openshift.teamsubmission',
    'openshift.node_manage',
    'openshift.messaging',
    'openshift.clarification',
    'openshift.helpFunctions',
    'openshift.judge_supervise',

)

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


ROOT_URLCONF = 'openshift.urls'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'openshift.wsgi.application'

TEMPLATE_DIRS = (
     os.path.join(BASE_DIR,'templates'),
)



MYSQL = True
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if MYSQL:
    DATABASES = {
         'default': {
             'ENGINE'	: 'django.db.backends.mysql',
             'NAME'	: 'gentleidi',
             'USER'	: os.getenv('USER'), #Added Windows support  
	     'PASSWORD'	: 'password',
	     'HOST'	: 'localhost',
	     'PORT'	: '3306',

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
LOG_ROOT = os.path.join(BASE_DIR, '..' , 'log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
	    'formatter': 'verbose',
            'filename': LOG_ROOT + '/debug.log',
        },
    },
    'loggers': {
        'idiopen': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
	'django': {
	    'handlers': ['file'],
	    'level': 'INFO',
	    'propagate': True,
	},
    },
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

