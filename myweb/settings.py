"""
Django settings for myweb project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0k3^xbe$m)*r@9)97=-vt097ag^45ln1ort7wa@n03%x9*h3sk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*",]

VERSION = 'v1.0.12'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.myapp',
    #'apps.upload',
    #'apps.monitor',
    #'apps.app01',
    #'rest_framework',
    #'apps.DjangoUeditor',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
   # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myweb.urls'

'''
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
'''
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'loonflow.contexts.global_variables',
            ],
        #'libraries':{
        #            'loonflow_filter': 'apps.manage.templatetags.loonflow_filter',

        #            }
        },
    },
]
WSGI_APPLICATION = 'myweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_test',
        'USER': 'root',
        'PASSWORD': 'redhat',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'
#LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

#USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
'''
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
'''
'''
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR,"templates")
]
'''

### static

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    #     ("css", os.path.join(STATIC_ROOT,'css')),

    ("bower_components", os.path.join(STATIC_ROOT, 'bower_components')),
    ("dist", os.path.join(STATIC_ROOT, 'dist')),
    ("plugins", os.path.join(STATIC_ROOT, 'plugins')),
    ("extra",os.path.join(STATIC_ROOT,'extra')),

    # ("js", os.path.join(STATIC_ROOT, 'js')),
    # ("image", os.path.join(STATIC_ROOT, 'image')),
    # ("css", os.path.join(STATIC_ROOT, 'css')),
    # ("dist", os.path.join(STATIC_ROOT, 'dist')),
    # ("plugins", os.path.join(STATIC_ROOT, 'plugins')),
    # ("fonts", os.path.join(STATIC_ROOT, 'fonts')),
    # ("font-awesome", os.path.join(STATIC_ROOT, 'font-awesome')),
    # ("img", os.path.join(STATIC_ROOT, 'img')),
    # ("bootstrap", os.path.join(STATIC_ROOT, 'bootstrap')),
    # ("apps/ueditor", os.path.join(STATIC_ROOT, 'ueditor')),
    # ("echarts", os.path.join(STATIC_ROOT, 'echarts')),
    # ("ueditor", os.path.join(STATIC_ROOT, 'ueditor')),
    # ("ventor", os.path.join(STATIC_ROOT, 'ventor')),
)

### media

MEDIA_ROOT = [
    os.path.join(BASE_DIR,"media")
]
MEDIA_URL = '/media/'
MEDIAFILES_DIRS = [
    os.path.join(BASE_DIR,"media")
]

### session

#SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'   #浏览器cook（相当于没有用session，又把敏感信息保存到客户端了）
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'        #缓存 redis memcache
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'        #缓存 redis memcache  +db
SESSION_CACHE_ALIAS = "default"
#SESSION_ENGINE = 'django.contrib.sessions.backends.file'             #文件
#SESSION_FILE_PATH = 文件路径
#SESSION_ENGINE = 'django.contrib.sessions.backends.db'                #默认数据库存储
######  pip install django-redis-sessions  使用第三方库貌似指定库不起作用，存储在0，prefix也没起作用#######
#SESSION_ENGINE = 'redis_sessions.session'
#SESSION_REDIS_HOST = 'localhost'
#SESSION_REDIS_PORT = 6379
#SESSION_REDIS_DB = 2
#SESSION_REDIS_PASSWORD = ''
#SESSION_REDIS_PREFIX = 'session'
##########################################
SESSION_COOKIE_NAME="sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
SESSION_COOKIE_PATH="/"          # Session的cookie保存的路径
SESSION_COOKIE_DOMAIN = None     # Session的cookie保存的域名
SESSION_COOKIE_SECURE = False    # 是否Https传输cookie
SESSION_COOKIE_HTTPONLY = True   # 是否Session的cookie只支持http传输
SESSION_COOKIE_AGE = 60*30       # Session的cookie失效日期（2周） 默认1209600秒
SESSION_EXPIRE_AT_BROWSER_CLOSE =True  # 是否关闭浏览器使得Session过期

SESSION_SAVE_EVERY_REQUEST = True      #如果你设置了session的过期时间 30分钟后，这个参数是False30分钟过后，session准时失效
#如果设置 True，在30分钟期间有请求服务端，就不会过期！（为什么逛一晚上淘宝，也不会登出，但是不浏览器不刷新了就会自动登出）



### rest-framework

'''
REST_FRAMEWORK = {
     #Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
'''

### email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False   #是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = False    #是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'smtp.qq.com'   #发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 25     #发件箱的SMTP服务器端口
EMAIL_HOST_USER = 'xxx@qq.com'    #发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'xxx'         #发送邮件的邮箱密码(这里使用的是授权码)

### cache
# pip install django-redis-cache(Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)] on win32
# Django 2.1.7 #django-redis-cache  3.0.0 #redis:3.5.3)

CACHES={
    'default': {
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', #缓存到本地内存中
        "BACKEND": "redis_cache.cache.RedisCache",  #缓存到redis中
        "LOCATION": "localhost:6379",               #默认database：1
        'TIMEOUT': 600, #默认5分钟
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
            "PASSWORD":"",},
    }
}

'''
# pip install django-redis（python:3.5.3,django:2.2.17,django-redis:3.5.0,redis:3.5.3）
CACHES={
    'default': {
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', #缓存到本地内存中
        "BACKEND": "django_redis.cache.RedisCache",  #缓存到redis中
        "LOCATION": "redis://localhost:6379/1",
        'TIMEOUT': 600, #默认5分钟
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
            "PASSWORD":"",},
    }
}
'''

### celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_TASK_SERIALIZER = 'json'

### zabbix
ZABBIX_URL = 'http://1.1.1.1/zabbix'
ZABBIX_USER = 'xxx'
ZABBIX_PASSWORD = 'xxx'

### prometheus
PROM_URL = 'http://1.1.1.1/prometheus'
PROM_USER = 'xxx'
PROM_PASSWROD = 'xxx'

### gitlab
GITLAB_URL = 'http://1.1.1.1'
GITLAB_TOKEN = 'xxx'

###
AUTH_USER_MODEL = "myapp.userInfo"
