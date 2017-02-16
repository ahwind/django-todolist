
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '7e30zz-%m%dduk=^$ju0kh-22sv%0z$_94926$jix-$q2_lkt)'

DEBUG = True

ALLOWED_HOSTS = ['*']


EXCLUDE_USER = ['admin']

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'todo.middleware.CheckUserSiteMiddleware',
]


ROOT_URLCONF = 'todolist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'todo.context_processors.box',
            ],
        },
    },
]

WSGI_APPLICATION = 'todolist.wsgi.application'

REDISCACHE = {
    'HOST': '192.168.10.14',
    'PORT': '6379',
    'PASSWD': '',
    'DB': '0'
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'todo_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '192.168.10.14',
        'PORT': '3306',
        'OPTIONS': {
         "init_command": "SET default_storage_engine=INNODB,FOREIGN_KEY_CHECKS=0",
        }
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


TIME_ZONE = 'Asia/Shanghai'

DEFAULT_CHARSET = 'utf-8'

LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = 'http://static.example.com/'

STATIC_ROOT = "static/"

MEDIA_ROOT = 'media/'
MEDIA_URL = 'media/'

