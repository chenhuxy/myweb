"""
Django settings for myweb project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0k3^xbe$m)*r@9)97=-vt097ag^45ln1ort7wa@n03%x9*h3sk'

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = True

DEBUG = False

ALLOWED_HOSTS = ["*", ]

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
    # 'rest_framework',
    # 'apps.DjangoUeditor',
    'channels',  # websocket使用

]

# 日志配置

log_path = os.path.join(BASE_DIR, 'logs')  # log_path是存放日志的路径
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
	# 简单格式
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 100,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'info', 'console', 'default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# 指定ASGI的路由地址

# channels运行于ASGI协议上，ASGI的全名是Asynchronous Server Gateway Interface。它是区别于Django使用的WSGI协议 的一种异步服务网关接口协议，
# 正是因为它才实现了websocket
# ASGI_APPLICATION 指定主路由的位置为webapp下的routing.py文件中的application

ASGI_APPLICATION = 'myweb.routing.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义操作日志记录中间件
    'apps.middlewares.LogMiddleware.OpLog',
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
            ],
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
        'NAME': 'myweb',
        'USER': 'myweb',
        'PASSWORD': 'myweb',
        'HOST': 'mysql',
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
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/cmdb/static/'
'''
# settings中debug开启时，加载静态文件使用
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
'''
# settings中debug关闭时，加载静态文件使用
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# session配置

# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'   #浏览器cook（相当于没有用session，又把敏感信息保存到客户端了）
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'        #缓存 redis memcache
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # 缓存 redis memcache  +db
SESSION_CACHE_ALIAS = "default"
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'             #文件
# SESSION_FILE_PATH = 文件路径
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'                #默认数据库存储
######  pip install django-redis-sessions  使用第三方库貌似指定库不起作用，存储在0，prefix也没起作用#######
# SESSION_ENGINE = 'redis_sessions.session'
# SESSION_REDIS_HOST = 'localhost'
# SESSION_REDIS_PORT = 6379
# SESSION_REDIS_DB = 2
# SESSION_REDIS_PASSWORD = ''
# SESSION_REDIS_PREFIX = 'session'
##########################################
SESSION_COOKIE_NAME = "sessionid"  # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输
SESSION_COOKIE_AGE = 60 * 30  # Session的cookie失效日期（2周） 默认1209600秒
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期
SESSION_SAVE_EVERY_REQUEST = True  # 如果你设置了session的过期时间 30分钟后，这个参数是False30分钟过后，session准时失效
# 如果设置 True，在30分钟期间有请求服务端，就不会过期！（为什么逛一晚上淘宝，也不会登出，但是不浏览器不刷新了就会自动登出）


# rest-framework配置

'''
REST_FRAMEWORK = {
     #Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
'''

# email配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False  # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = False  # 是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'xxx'  # 发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 25  # 发件箱的SMTP服务器端口
EMAIL_HOST_USER = 'xxx'  # 发送邮件的邮箱用户名
EMAIL_HOST_PASSWORD = 'xxx'  # 发送邮件的邮箱密码(这里使用的是授权码)
EMAIL_SEND_FROM = 'xxx'  # 发送邮件的邮箱地址

# cache配置
# pip install django-redis-cache(Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (
# AMD64)] on win32 Django 2.1.7 #django-redis-cache  3.0.0 #redis:3.5.3)

CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', #缓存到本地内存中
        "BACKEND": "redis_cache.cache.RedisCache",  # 缓存到redis中
        "LOCATION": "redis:6379",  # 默认database：1
        'TIMEOUT': 600,  # 默认5分钟
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
            "PASSWORD": "", },
    }
}

'''
# pip install django-redis（python:3.5.3,django:2.2.17,django-redis:3.5.0,redis:3.5.3）
CACHES = {
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

# celery配置
CELERY_BROKER_URL = 'redis://redis:6379/2'
CELERY_RESULT_BACKEND = 'redis://redis:6379/2'
CELERY_TASK_SERIALIZER = 'json'

# zabbix配置
ZABBIX_URL = 'http://10.180.10.84/zabbix'
ZABBIX_USER = 'xxx'
ZABBIX_PASSWORD = 'xxx'

# prometheus配置
PROM_URL = 'http://xxx'
PROM_USER = 'xxx'
PROM_PASSWROD = 'xxx'
PROM_DINGTALK_WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
# 测试
# PROM_WELINK_WEBHOOK_URL = 'https://open.welink.huaweicloud.com/api/werobot/v1/webhook/send?token=xxx&channel=standard'
# PROM_WELINK_UUID = "181778b68d784679ac3d71d5a09fec86"
# 生产
PROM_WELINK_WEBHOOK_URL = 'https://open.welink.huaweicloud.com/api/werobot/v1/webhook/send?token=xxx&channel=standard'
PROM_WELINK_UUID = "efe21978936a4122bdb2b8fa73b3bc88"

# gitlab配置
GITLAB_URL = 'http://xxx'
GITLAB_TOKEN = 'xxx'

# 自定义用户表配置
AUTH_USER_MODEL = "myapp.userInfo"

# websocket配置
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}
"""
CHANNEL_LAYERS = {
     "default": {
         "BACKEND": "channels.layers.InMemoryChannelLayer",
     }
}
"""

# ssh配置
SSH_HOST = '192.168.38.129'
SSH_PORT = 22
SSH_USERNAME = 'root'
SSH_PASSWORD = 'redhat'
SSH_WORKDIR = '/root/gitlab/download'
SSH_SCRIPT_NAME = 'auto-OneKeyDeploy'
SSH_CMD = 'cd ' + SSH_WORKDIR + '&& python ' + SSH_SCRIPT_NAME + '.py'

# WORKFLOW_EMAIL 配置
EXTERNAL_URL = 'http://ip:8000'
WF_EMAIL_SUBJECT = '【运维发布系统流程审批提醒】'
ACTIVE_EMAIL_SUBJECT = '【运维发布系统账号激活邮件】'
VERIFY_CODE_EMAIL_SUBJECT = '【运维发布系统找回密码邮件】'

# SKYWALKING_EMAIL 配置
SKYWALKING_EMAIL_SUBJECT = '【Skywalking链路监控告警】'
SKYWALKING_EMAIL_RECEIVER = 'xxx,xxx'  # 添加更多的收件人邮箱,用逗号分割
SKYWALKING_DINGTALK_WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
# 测试
# SKYWALKING_WELINK_WEBHOOK_URL = 'https://open.welink.huaweicloud.com/api/werobot/v1/webhook/send?token=xxx&channel=standard'
# SKYWALKING_WELINK_UUID = "181778b68d784679ac3d71d5a09fec86"
# 生产
SKYWALKING_WELINK_WEBHOOK_URL = 'https://open.welink.huaweicloud.com/api/werobot/v1/webhook/send?token=xxx&channel=standard'
SKYWALKING_WELINK_UUID = "ab1c18520f2b4728bee5943b2a3e9046"

# secret
API_SECRET = 'yYEtEMvGMVmCaxpOWIjOWjtvTk'

# 定义接口请求超时时间
API_ACCESS_TIMEOUT = 3000  # ms
