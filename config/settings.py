import os
from datetime import timedelta
from pathlib import Path
import environ

AUTH_USER_MODEL = 'users.User'
# чтобы вместо логина можно прописывать username, mail, phone_number
AUTHENTICATION_BACKENDS = ('src.users.backends.AuthBackend',)

root = environ.Path(__file__) - 2

# print(root)

env = environ.Env()

environ.Env.read_env(env.str(root(), '.env'))

BASE_DIR = root()

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', True)
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', default='').split(' ')
DOMAIN_NAME = env.str('DOMAIN_NAME')

TOKEN = env.str('TOKEN')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken', # Для использования стандартной библиотеки авторизации по токенам
    'djoser',
    'corsheaders',
    'phonenumber_field',

    'src.users', # прописываем самым первым для переопределения юзера
    'api',
    'src.telegram',
    'src.common',

    'drf_spectacular', # после всех приложений ставится
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('PG_DATABASE', default='postgres'),
        'USER': env.str('PG_USER', default='postgres'),
        'PASSWORD': env.str('PG_PASSWORD', default='1'),
        'HOST': env.str('DB_HOST', default='localhost'),
        'PORT': env.int('DB_PORT', default=5432),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
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

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATIC AND MEDIA====================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# DRF =======================================================================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ( # Кто имеет доступ
        # 'rest_framework.permissions.IsAdminUser', # Администратор
        'rest_framework.permissions.AllowAny', # Все
    ),
    'DEFAULT_RENDERER_CLASSES': [
        # Настройка рендера для отправки на фронт и получение на бэк в JSON
        'rest_framework.renderers.JSONRenderer',
        # для отображения данных в шаблоне rest_framework
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [ # Аутентификация
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication', # Для JWT регистрации
        'rest_framework.authentication.TokenAuthentication', # по токену Для Djoser
        'rest_framework.authentication.BasicAuthentication', # Базовая
        'rest_framework.authentication.SessionAuthentication' # Для session, например что бы зайти в админку
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
}

# CORS HEADERS===============================================
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False

# SPECTACULAR===============================================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'DjangoDRFTelegram',
    'DESCRIPTION': 'DjangoDRFTelegram',
    'VERSION': '1.0.0',

    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'SERVE_AUTHENTICATION': [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],

    'SWAGGER_UI_SETTINGS': {
        'DeepLinking': True,
        'DisplayOperationId': True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}

# Djoser====================================================================
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}', # для подтверждения сброса пароля
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}', # для сброса пользователя
    'ACTIVATION_URL': '#/activate/{uid}/{token}', # для активации
    'SEND_ACTIVATION_EMAIL': True, # отправка емаил True
    'SERIALIZERS': {},
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',), # смотрит JWT токен в хедере со значением Bearer
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}
# EMAIL ======================================================================

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # для отправки в консоль
else:
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    KEY_MAIL = env.str('KEY_MAIL') # Загружаем из .env
    EMAIL_HOST = 'smtp.mail.ru'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'chausovo@mail.ru' # Почта отправителя
    EMAIL_HOST_PASSWORD = KEY_MAIL # Пароль для внешнего приложения
    EMAIL_USE_TLS = False # Шифрование TSL
    EMAIL_USE_SSL = True # Шифрование SSL
    DEFAULT_FROM_EMAIL = 'django-auth@Kantegory.me' # как бы генерирует разные почтовые ящики

# Для вывода ORM запросов в консоль===========================
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG'
            }
        }
}

