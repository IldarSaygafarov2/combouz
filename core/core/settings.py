from collections import OrderedDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-pt495=&=psj+i&wua*4mh026y5n7y4%72=$tj+lhh(sm@osl_v'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
    'constance',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates"
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = ['app.backends.EmailBackend']

AUTH_USER_MODEL = "app.CustomUser"
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CART_SESSION_ID = "cart"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 28

BOT_TOKEN = "6651100598:AAE0CSIZJ4D9JX-DRnGk_qTYdJ2WX-bzrb8"
CHANNEL_ID = -1001965630465
CHANNEL_API_LINK = "https://api.telegram.org/bot{token}/sendMessage?chat_id={channel_id}&text={text}"


CONSTANCE_BACKEND = 'constance.backends.memory.MemoryBackend'

CONSTANCE_CONFIG = OrderedDict([
    ('EMAIL', ('info@combo.uz', 'Почта для связи')),
    ('PHONE_NUMBER', ('+998 (95) 142 - 33 - 13', 'Номер для связи')),
    ('OFFICE_ADDRESS', ('г.Ташкент, Алмазарский район, ул.Сагбан 37/1', 'Локация офиса')),
    ('WORKING_TIME', ('с 9:00 до 19:00', 'Режим работы')),
    ('CALLING_TIME', ('с 8:00 до 20:00', 'Режим звонков')),
    ('INSTAGRAM_LINK', ('', 'Ссылка на аккаунт instagram')),
    ('FACEBOOK_LINK', ('', 'Ссылка на аккаунт facebook')),
    ('TELEGRAM_LINK', ('', 'Ссылка на аккаунт telegram')),
])


CONSTANCE_CONFIG_FIELDSETS = {
    'Общие данные': ('EMAIL', 'PHONE_NUMBER', 'OFFICE_ADDRESS',  'WORKING_TIME', 'CALLING_TIME'),
    'Социальные сети': ('INSTAGRAM_LINK', 'FACEBOOK_LINK', 'TELEGRAM_LINK'),
    # 'Theme Options': ('THEME',),
}