import os.path
import random
import string
from celery.schedules import crontab

import base64

_basedir = os.path.abspath(os.path.dirname(__file__))

# See the Lemur docs (https://lemur.readthedocs.org) for more information on configuration

LOG_LEVEL = str(os.environ.get('LOG_LEVEL','DEBUG'))
LOG_FILE = str(os.environ.get('LOG_FILE','/home/lemur/.lemur/lemur.log'))
LOG_JSON = True

CORS = os.environ.get("CORS") == "True"
debug = os.environ.get("DEBUG") == "True"

def get_random_secret(length):
    secret_key = ''.join(random.choice(string.ascii_uppercase) for x in range(round(length / 4)))
    secret_key = secret_key + ''.join(random.choice("~!@#$%^&*()_+") for x in range(round(length / 4)))
    secret_key = secret_key + ''.join(random.choice(string.ascii_lowercase) for x in range(round(length / 4)))
    return secret_key + ''.join(random.choice(string.digits) for x in range(round(length / 4)))

# this is the secret key used by flask session management
SECRET_KEY = repr(os.environ.get('SECRET_KEY', get_random_secret(32).encode('utf8')))

# You should consider storing these separately from your config
LEMUR_TOKEN_SECRET = repr(os.environ.get('LEMUR_TOKEN_SECRET',
                                         base64.b64encode(get_random_secret(32).encode('utf8'))))
# This must match the key for whichever DB the container is using - this could be a dump of dev or test, or a unique key
LEMUR_ENCRYPTION_KEYS = repr(os.environ.get('LEMUR_ENCRYPTION_KEYS',
                                            base64.b64encode(get_random_secret(32).encode('utf8')).decode('utf8')))


REDIS_HOST = 'docker.for.mac.localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CELERY_RESULT_BACKEND = 'redis://docker.for.mac.localhost:6379'
CELERY_BROKER_URL = 'redis://docker.for.mac.localhost:6379'
CELERY_IMPORTS = ('lemur.common.celery')
CELERYBEAT_SCHEDULE = {
    # 'fetch_all_pending_acme_certs': {
    #     'task': 'lemur.common.celery.fetch_all_pending_acme_certs',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*"),
    # },
    # 'remove_old_acme_certs': {
    #     'task': 'lemur.common.celery.remove_old_acme_certs',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=7, minute=30, day_of_week=1),
    # },
    # 'clean_all_sources': {
    #     'task': 'lemur.common.celery.clean_all_sources',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour=1, minute=0, day_of_week=1),
    # },
    # 'sync_all_sources': {
    #     'task': 'lemur.common.celery.sync_all_sources',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="*/2", minute=5),
    #     # this job is running 25min before endpoints_expire which deletes endpoints which were not updated
    # },
    # 'sync_source_destination': {
    #     'task': 'lemur.common.celery.sync_source_destination',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="*/2", minute=15),
    # },
    # 'report_celery_last_success_metrics': {
    #     'task': 'lemur.common.celery.report_celery_last_success_metrics',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*"),
    # },
    # 'certificate_reissue': {
    #     'task': 'lemur.common.celery.certificate_reissue',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="18", minute=0),
    # },
    # 'certificate_rotate': {
    #     'task': 'lemur.common.celery.certificate_rotate',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="19", minute=0),
    # },
    # 'endpoints_expire': {
    #     'task': 'lemur.common.celery.endpoints_expire',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="*/2", minute=30),
    #     # this job is running 25min after sync_all_sources which updates endpoints
    # },
    # 'get_all_zones': {
    #     'task': 'lemur.common.celery.get_all_zones',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*/30"),
    # },
    # 'check_revoked': {
    #     'task': 'lemur.common.celery.check_revoked',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(hour="21", minute=0),
    # }
    # This shall not run in TEST, due to imported certificates and the conflicting auto-rotate
    #    'enable_autorotate_for_certs_attached_to_endpoint': {
    #        'task': 'lemur.common.celery.enable_autorotate_for_certs_attached_to_endpoint',
    #        'options': {
    #            'expires': 180
    #        },
    #        'schedule': crontab(hour="20", minute=0),
    #    }
    # 'notify_expirations': {
    #     'task': 'lemur.common.celery.notify_expirations',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*"),
    #  },
    # 'notify_authority_expirations': {
    #     'task': 'lemur.common.celery.notify_authority_expirations',
    #     'options': {
    #         'expires': 180
    #     },
    #     'schedule': crontab(minute="*"),
    # }
}
CELERY_TIMEZONE = 'UTC'

SQLALCHEMY_ENABLE_FLASK_REPLICATED = False
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI','postgresql://lemur:lemur@localhost:5432/lemur')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 499
SQLALCHEMY_POOL_TIMEOUT = 20

LEMUR_EMAIL = 'lemur@example.com'
LEMUR_SECURITY_TEAM_EMAIL = ['security@example.com']
LEMUR_SECURITY_TEAM_EMAIL_INTERVALS = [15, 2]
LEMUR_DEFAULT_EXPIRATION_NOTIFICATION_INTERVALS = [30, 15, 2]
LEMUR_EMAIL_SENDER = 'smtp'

# mail configuration
# MAIL_SERVER = 'mail.example.com'

PUBLIC_CA_MAX_VALIDITY_DAYS = 397
DEFAULT_VALIDITY_DAYS = 365

LEMUR_OWNER_EMAIL_IN_SUBJECT = False


LEMUR_DEFAULT_COUNTRY = str(os.environ.get('LEMUR_DEFAULT_COUNTRY','US'))
LEMUR_DEFAULT_STATE = str(os.environ.get('LEMUR_DEFAULT_STATE','California'))
LEMUR_DEFAULT_LOCATION = str(os.environ.get('LEMUR_DEFAULT_LOCATION','Los Gatos'))
LEMUR_DEFAULT_ORGANIZATION = str(os.environ.get('LEMUR_DEFAULT_ORGANIZATION','Example, Inc.'))
LEMUR_DEFAULT_ORGANIZATIONAL_UNIT = str(os.environ.get('LEMUR_DEFAULT_ORGANIZATIONAL_UNIT','Example'))

LEMUR_DEFAULT_AUTHORITY = str(os.environ.get('LEMUR_DEFAULT_AUTHORITY','DigiCertInc'))

LEMUR_DEFAULT_ROLE = 'operator'

# this is a list of domains as regexes that only admins can issue
LEMUR_RESTRICTED_DOMAINS = []

ACTIVE_PROVIDERS = []
METRIC_PROVIDERS = []

# Authority Settings - These will change depending on which authorities you are
# using
current_path = os.path.dirname(os.path.realpath(__file__))

# DNS Settings

# exclude logging missing SAN, since we can have certs from private CAs with only cn, prod parity
LOG_SSL_SUBJ_ALT_NAME_ERRORS = False

ACME_DNS_PROVIDER_TYPES = {"items": [
    {
        'name': 'route53',
        'requirements': [
            {
                'name': 'account_id',
                'type': 'int',
                'required': True,
                'helpMessage': 'AWS Account number'
            },
        ]
    },
    {
        'name': 'cloudflare',
        'requirements': [
            {
                'name': 'email',
                'type': 'str',
                'required': True,
                'helpMessage': 'Cloudflare Email'
            },
            {
                'name': 'key',
                'type': 'str',
                'required': True,
                'helpMessage': 'Cloudflare Key'
            },
        ]
    },
    {
        'name': 'dyn',
    },
    {
        'name': 'ultradns',
    },
]}

# Authority plugins which support revocation
SUPPORTED_REVOCATION_AUTHORITY_PLUGINS = ['digicert-cis-issuer', 'acme-issuer']
