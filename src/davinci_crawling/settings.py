# -*- coding: utf-8 -*-
# Copyright (c) 2019 BuildGroup Data Services Inc.

"""
Django settings for DaVinci Crawling Framwork.
"""

import os
import sys

try:
    from dse import ConsistencyLevel
except ImportError:
    from cassandra import ConsistencyLevel

from configurations import Configuration


class Common(Configuration):

    CARAVAGGIO_API_TITLE = "DaVinci Crawling API"
    CARAVAGGIO_API_VERSION = "v1"
    CARAVAGGIO_API_DESCRIPTION = "API for DaVinci Crawling applications"
    CARAVAGGIO_API_TERMS_URL = "https://www.google.com/policies/terms/"
    CARAVAGGIO_API_CONTACT = "contact@buildgroupai.com"
    CARAVAGGIO_API_LICENSE = "BSD License"

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "2w=es4^%3i4n2cya(0)ws&bq+@h)m1nepzkvd&pi+wvgsue%ms")

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = os.getenv("DEBUG", "False") == "True"

    ADMINS = (
        # ('Your Name', 'your_email@example.com'),
    )

    MANAGERS = ADMINS

    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "dev@domain.com")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "***")

    DSE_SUPPORT = os.getenv("DSE_SUPPORT", "True") == "True"

    # SECURITY WARNING: App Engine's security features ensure that it is safe
    # to have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a
    # Django app not on App Engine, make sure to set an appropriate host here.
    # See https://docs.djangoproject.com/en/1.10/ref/settings/
    ALLOWED_HOSTS = ["*"]

    INTERNAL_IPS = []

    # Application definition

    INSTALLED_APPS = [
        'django_cassandra_engine',
        'django_cassandra_engine.sessions',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        # 'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Comment the next line to disable the admin:
        'django.contrib.admin',
        # Comment the next line to disable admin documentation:
        'django.contrib.admindocs',
        'rest_framework',
        'rest_framework_filters',
        'rest_framework.authtoken',
        'rest_framework_cache',
        'drf_yasg',
        'haystack',
        'caravaggio_rest_api',
        'caravaggio_rest_api.logging',
        'caravaggio_rest_api.users',
        'davinci_crawling',
        'davinci_crawling.task'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'davinci_crawling.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'davinci_crawling/templates'),
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'davinci_crawling.wsgi.application'

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING_FILE = os.getenv("LOGGING_FILE", "/data/davinci_crawling/"
                                             "log/davinci_crawling-debug.log")
    LOGGING_DIR = "/".join(LOGGING_FILE.split("/")[:-1])

    # All the fixed settings that a crawler can have, every crawler should
    # add their specific params here
    DAVINCI_CONF = {
        "default": {
            "verbosity": 1,
            "no_color": False,
            "force_color": False,
            "local_dir": "fs://%s/log/local" % LOGGING_DIR,
            "cache_dir": "fs://%s/log/cache" % LOGGING_DIR,
            "workers_num": 10,
            'chromium_bin_file':
                '/Applications/Chromium.app/Contents/MacOS/Chromium',
            'io_gs_project': 'centering-badge-212119',
        },
        "bovespa": {
            'companies_listing_update_elapsetime': 30,
            'companies_files_update_elapsetime': 30
        }
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format':
                    '%(levelname)s %(asctime)s %(module)s %(process)d '
                    '%(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'debug_log': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_FILE,
                'maxBytes': 1024 * 1024 * 100,
                'backupCount': 1,
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django_cassandra_engine': {
                'handlers': ['console', 'debug_log', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'caravaggio_rest_api': {
                'handlers': ['console', 'debug_log', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'davinci_crawling': {
                'handlers': ['console', 'debug_log', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'davinci_crawler_crawler_11': {
                'handlers': ['console', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': True,
            }
        }
    }

    # Database

    # Check to see if MySQLdb is available; if not, have pymysql masquerade as
    # MySQLdb. This is a convenience feature for developers who cannot install
    # MySQLdb locally; when running in production on Google App Engine Standard
    # Environment, MySQLdb will be used.
    # try:
    #    import MySQLdb  # noqa: F401
    # except ImportError:
    #    import pymysql
    #    pymysql.install_as_MySQLdb()

    # [START db_setup]
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "6543")
    DB_NAME = os.getenv("DB_NAME", "davinci")
    DB_USER = os.getenv("DB_USER", "davinci")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "davinci")

    CASSANDRA_DB_HOST = os.getenv(
        "CASSANDRA_DB_HOST", "127.0.0.1,127.0.0.2,127.0.0.3")
    CASSANDRA_DB_NAME = os.getenv("CASSANDRA_DB_NAME", "davinci")
    CASSANDRA_DB_USER = os.getenv("CASSANDRA_DB_USER", "davinci")
    CASSANDRA_DB_PASSWORD = os.getenv("CASSANDRA_DB_PASSWORD", "davinci")
    CASSANDRA_DB_STRATEGY = os.getenv("CASSANDRA_DB_STRATEGY",
                                      "SimpleStrategy")
    CASSANDRA_DB_REPLICATION = os.getenv("CASSANDRA_DB_REPLICATION", 1)

    try:
        from dse.cqlengine import models
    except ImportError:
        from cassandra.cqlengine import models

    models.DEFAULT_KEYSPACE = CASSANDRA_DB_NAME

    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
        },
        'cassandra': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': CASSANDRA_DB_NAME,
            'TEST': {
                'NAME': "test_{}".format(CASSANDRA_DB_NAME)
            },
            'HOST': CASSANDRA_DB_HOST,
            'USER': CASSANDRA_DB_USER,
            'PASSWORD': CASSANDRA_DB_PASSWORD,
            'OPTIONS': {
                'replication': {
                    'strategy_class': CASSANDRA_DB_STRATEGY,
                    'replication_factor': CASSANDRA_DB_REPLICATION
                },
                'connection': {
                    'consistency': ConsistencyLevel.LOCAL_ONE,
                    'retry_connect': True
                    # + All connection options for cassandra.cluster.Cluster()
                },
                'session': {
                    'default_timeout': 10,
                    'default_fetch_size': 10000
                    # + All options for cassandra.cluster.Session()
                }
            }
        }
    }
    # [END db_setup]

    # Password validation
    # https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'NumericPasswordValidator',
        },
    ]

    # Internationalization

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # In a Windows environment this must be set to your system time zone.
    TIME_ZONE = "UTC"

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = "en-us"

    SITE_ID = 1

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = True

    # If you set this to False, Django will not format dates, numbers and
    # calendars according to the current locale.
    USE_L10N = True

    # If you set this to False, Django will not use timezone-aware datetimes.
    USE_TZ = True

    # Absolute filesystem path to the directory that will hold user-uploaded
    # files. Example: "/home/media/media.lawrence.com/media/"
    MEDIA_ROOT = ''

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
    MEDIA_URL = ''

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.8/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR + '/davinci_crawling/static')

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.8/howto/static-files/
    # STATIC_URL = '/static/'
    STATIC_URL = os.getenv('STATIC_URL', '/static/')

    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(BASE_DIR + '/davinci_crawling/task/static'),
    )

    # List of finder classes that know how to find static files in
    # various locations.
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

    REST_FRAMEWORK = {
        'PAGE_SIZE': 10,
        'DEFAULT_PAGINATION_CLASS':
            'rest_framework.pagination.PageNumberPagination',

        'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle',
            'rest_framework.throttling.ScopedRateThrottle'
        ),

        'DEFAULT_THROTTLE_RATES': {
            'anon': '100/day',
            'user': '60/minute'
        },

        # The name of the alternative query string  be can use for authenticate
        # users in each request
        # Ex. http://mydomain.com/users/user/?auth_token=<token_key>"
        'QUERY_STRING_AUTH_TOKEN': "auth_token",

        # Do we want to log any access made to the API?
        'LOG_ACCESSES': True,

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_AUTHENTICATION_CLASSES': (
            # 'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            'caravaggio_rest_api.drf.authentication.TokenAuthSupportQueryString',
        ),

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
            'rest_framework.permissions.IsAuthenticated'
        ],
        # REST framework also includes support for generic filtering backends
        # that allow you to easily construct complex searches and filters
        'DEFAULT_FILTER_BACKENDS':
            ('drf_haystack.filters.HaystackFilter',
             'drf_haystack.filters.HaystackBoostFilter',
             'drf_haystack.filters.HaystackOrderingFilter',),

        'TEST_REQUEST_DEFAULT_FORMAT': 'json',

        'ORDERING_PARAM': 'order_by',

        # https://www.django-rest-framework.org/api-guide/fields/#decimalfield
        # To use decimal as representation by default
        'COERCE_DECIMAL_TO_STRING': False
    }

    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_AUTHENTICATION_METHOD = 'email'

    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_USER_EMAIL_FIELD = 'email'
    ACCOUNT_LOGOUT_ON_GET = True

    AUTH_USER_MODEL = 'users.CaravaggioUser'

    REST_AUTH_SERIALIZERS = {
        "USER_DETAILS_SERIALIZER":
            "caravaggio_rest_api.users.serializers."
            "CaravaggioUserDetailsSerializer",
    }
    REST_AUTH_REGISTER_SERIALIZERS = {
        "REGISTER_SERIALIZER":
            "caravaggio_rest_api.users.serializers."
            "CaravaggioUserRegisterSerializer",
    }

    SESSION_ENGINE = 'django_cassandra_engine.sessions.backends.db'
    CASSANDRA_FALLBACK_ORDER_BY_PYTHON = True

    # Enable/Disable throttling
    THROTTLE_ENABLED = os.getenv("THROTTLE_ENABLED", "False") == "True"

    GET_THROTTLE_RATE = "6000/minute"
    LIST_THROTTLE_RATE = "200/minute"
    POST_THROTTLE_RATE = "100/minute"
    PUT_THROTTLE_RATE = "100/minute"
    DELETE_THROTTLE_RATE = "60/minute"
    VALIDATE_THROTTLE_RATE = "60/minute"
    PATCH_THROTTLE_RATE = "100/minute"
    METADATA_THROTTLE_RATE = "6000/minute"
    FACETS_THROTTLE_RATE = "6000/minute"

    THROTTLE_OPERATIONS = {
        'retrieve': GET_THROTTLE_RATE,
        'highlight': GET_THROTTLE_RATE,
        'list': LIST_THROTTLE_RATE,
        'create': POST_THROTTLE_RATE,
        'update': PUT_THROTTLE_RATE,
        'destroy': DELETE_THROTTLE_RATE,
        'validate': VALIDATE_THROTTLE_RATE,
        'partial_update': PATCH_THROTTLE_RATE,
        'metadata': METADATA_THROTTLE_RATE,
        'facets': FACETS_THROTTLE_RATE
    }

    HAYSTACK_DJANGO_ID_FIELD = "id"

    HAYSTACK_KEYSPACE = CASSANDRA_DB_NAME
    if 'test' in sys.argv:
        HAYSTACK_KEYSPACE = "test_{}".format(HAYSTACK_KEYSPACE)

    HAYSTACK_URL = os.getenv("HAYSTACK_URL", "http://127.0.0.1:8983/solr")
    HAYSTACK_ADMIN_URL = os.getenv(
        "HAYSTACK_ADMIN_URL", "http://127.0.0.1:8983/solr/admin/cores")

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE':
                'caravaggio_rest_api.haystack.backends.'
                'solr_backend.CassandraSolrEngine',
            'URL': HAYSTACK_URL,
            'KEYSPACE': HAYSTACK_KEYSPACE,
            'ADMIN_URL': HAYSTACK_ADMIN_URL,
            'BATCH_SIZE': 100,
            'INCLUDE_SPELLING': True,
            "DISTANCE_AVAILABLE": True,
        },
    }

    # Caching: Redis backend for caching

    REDIS_HOST_PRIMARY = os.getenv("REDIS_HOST_PRIMARY", "127.0.0.1")
    REDIS_PORT_PRIMARY = os.getenv("REDIS_PORT_PRIMARY", "6379")
    REDIS_PASS_PRIMARY = os.getenv("REDIS_PASS_PRIMARY", "")

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://{0}{1}:{2}/1".format(
                ":{0}@".format(REDIS_PASS_PRIMARY)
                if REDIS_PASS_PRIMARY else "",
                REDIS_HOST_PRIMARY, REDIS_PORT_PRIMARY),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "davinci_crawling"
        },
        'disk_cache': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/davinci_crawl_cache',
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 10000
            },
            "KEY_PREFIX": "davinci_crawling"
        },
        'mem_cache': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'davinci_crawling_cache',
            "KEY_PREFIX": "davinci_crawling"
        }
    }

    # DRF Caching
    REST_FRAMEWORK_CACHE = {
        # IMPORTANT: we need to use the default cache (REDIS) when we run
        # in a distributed environment. That is, many instances of the app
        # running separated. For instance: two or more balanced instances
        # of the REST API
        "DEFAULT_CACHE_BACKEND": 'default',
        "DEFAULT_CACHE_TIMEOUT": 86400,  # Default is 1 day
    }

    # Swagger Docs
    SWAGGER_SETTINGS = {
        'DEFAULT_INFO': 'davinci_crawling.views.api_info',
        'SECURITY_DEFINITIONS': {
            'api_key': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        },
        'LOGIN_URL': 'rest_framework:login',
        'LOGOUT_URL': 'rest_framework:logout',
        'DOC_EXPANSION': "none",
        'APIS_SORTER': 'alpha',
        'OPERATIONS_SORTER': None,
        'JSON_EDITOR': True,
        'USE_SESSION_AUTH': True,
        'SHOW_REQUEST_HEADERS': True,
        'SUPPORTED_SUBMIT_METHODS': [
            'get',
            'post',
            'put',
            'delete',
            'patch'
        ],
    }

    # APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default

    PROJECT_DOCKER_IMAGE = os.getenv(
        "PROJECT_DOCKER_IMAGE",
        "eu.gcr.io/dotted-ranger-212213/my-project:v0-0-1")

    DAVINCI_CRAWLERS_ENV_PARAMS = [
        "DSE_SUPPORT",
        "ENVIRONMENT",

        "CASSANDRA_DB_HOST",
        "CASSANDRA_DB_NAME",
        "CASSANDRA_DB_PASSWORD",
        "CASSANDRA_DB_REPLICATION",
        "CASSANDRA_DB_STRATEGY",
        "CASSANDRA_DB_USER",

        "DB_HOST",
        "DB_NAME",
        "DB_PASSWORD",
        "DB_PORT",
        "DB_USER",
        "DB_USER",

        "HAYSTACK_ACTIVE",
        "HAYSTACK_ADMIN_URL",
        "HAYSTACK_KEYSPACE",
        "HAYSTACK_URL",

        "REDIS_HOST_PRIMARY",
        "REDIS_PASS_PRIMARY",
        "REDIS_PORT_PRIMARY",

        "SECRET_KEY",
        "SECURE_SSL_HOST",
        "SECURE_SSL_REDIRECT",

        "STATIC_URL",
        "THROTTLE_ENABLED",

        "EMAIL_HOST_PASSWORD",
        "EMAIL_HOST_USER",

        "GAE_SERVICE",

        "GOOGLE_ANALYTICS_ID"
    ]

    DAVINCI_CRAWLERS = {
        # "bovespa": {
        #    "deployment": {
        #        # Google Cloud Platform
        #        "cloud": "gcp",
        #        "project": "dotted-ranger-212213",  # Sandbox
        #        "zone": "europe-west2-a",

        #        # A list of available machine types can be found here:
        #        # https://cloud.google.com/compute/docs/machine-types
        #        "machine-type": "n1-standard-1",#
        #        # Container - Optimized OS
        #        # https://cloud.google.com/compute/docs/images?
        #        #   hl=es-419#os-compute-support
        #        "image": {
        #            "project": "cos-cloud",
        #            "family": "cos-stable"
        #        }
        #    },
        #    "arguments": {
        #        "cache-dir": "gs://vanggogh2_harvest"
        #    },
        #    "cron": "*/5 * * * *"
        # }
    }


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = os.getenv("DEBUG", "True") == "True"

    TESTS_TMP_DIR = "/tmp/davinci/tests"

    ALLOWED_HOSTS = []

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'django_extensions', 'debug_toolbar'
    ]

    INSTALLED_APPS += [
        # Add here the davinci crawlers (apps),
        'davinci_crawling.example.bovespa'
    ]

    Common.LOGGING["loggers"]['davinci_crawler_bovespa'] = {
        'handlers': ['console', 'debug_log', 'mail_admins'],
        'level': 'DEBUG',
        'propagate': True,
    }

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]

    Common.REST_FRAMEWORK['LOG_ACCESSES'] = False


class Staging(Common):
    """
    The in-staging settings.
    """
    # Databases

    # The docker container starts a PGBouncer server in local to manage
    # the pool of connections. We need to connect to the local pgbounce
    # server
    CASSANDRA_DB_STRATEGY = os.getenv(
        "CASSANDRA_DB_STRATEGY", "NetworkTopologyStrategy")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            "HOST": "127.0.0.1",
            "PORT": "6543",
            'NAME': Common.DB_NAME,
            'USER': Common.DB_USER,
            'PASSWORD': Common.DB_PASSWORD,
        },
        'cassandra': {
            'ENGINE': 'django_cassandra_engine',
            'NAME': Common.CASSANDRA_DB_NAME,
            'HOST': Common.CASSANDRA_DB_HOST,
            'USER': Common.CASSANDRA_DB_USER,
            'PASSWORD': Common.CASSANDRA_DB_PASSWORD,
            'OPTIONS': {
                'replication': {
                    'strategy_class': CASSANDRA_DB_STRATEGY,
                    'replication_factor': Common.CASSANDRA_DB_REPLICATION

                    # 'strategy_class': 'NetworkTopologyStrategy',
                    # 'datacenter1': N1,
                    # ...,
                    # 'datacenterN': Nn
                },
                'connection': {
                    'consistency': ConsistencyLevel.LOCAL_ONE,
                    'retry_connect': True
                    # + All connection options for cassandra.cluster.Cluster()
                },
                'session': {
                    'default_timeout': 10,
                    'default_fetch_size': 10000
                    # + All options for cassandra.cluster.Session()
                }
            }
        }
    }

    # Security
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', "False") == "True"
    USE_X_FORWARDED_HOST = SECURE_SSL_REDIRECT
    CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
    SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
    SECURE_BROWSER_XSS_FILTER = SECURE_SSL_REDIRECT
    SECURE_CONTENT_TYPE_NOSNIFF = SECURE_SSL_REDIRECT
    SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_SSL_REDIRECT
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_HOST = os.getenv('SECURE_SSL_HOST', None)
    SECURE_SSL_REDIRECT = SECURE_SSL_REDIRECT
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO',
                               "https" if SECURE_SSL_REDIRECT else "http")


class Production(Staging):
    """
    The in-production settings.
    """

    LOGGING_FILE = "/var/log/davinci_crawling-debug.log"
