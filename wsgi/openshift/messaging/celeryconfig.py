#import fabric.api
#fabric.api.env.celery_path = subprocess.check_output(["which", "celery"])[:-1]
#fabric.api.env.celery_path = "/home/andesil/test"


BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'

CELERY_IMPORTS = ['tasks', 'celeryapp']

CELERY_ROUTES = {
        'tasks.add': 'low-priority',
        }

CELERY_ANNOTATIONS = {
            'tasks.add': {'rate_limit': '10/m'}
            }
