"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-uup3h3g#9uh6!mkkiqg=8_)5@knc)8@$-ua5uqu(jw-tp=5tby"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework_simplejwt',
    'rest_framework',
    'django_filters',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',
    'cart',
    'goods',
    'order',
    'users',
    'ckeditor',
    'history',
    'drf_yasg',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 支持跨域请求
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "shop.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "web_shop",
        "USER": "root",
        "PASSWORD": "123456",
        "PORT": 3306,
        "HOST": "localhost"
    },
    # 'mongodb': {
    #     'ENGINE': 'django.db.backends.mongodb',
    #     'NAME': 'shop',
    #     'CLIENT': {
    #         'host': 'localhost',
    #         'port': 27017,
    #         # 如果需要认证，可以添加 'username': 'your_username', 'password': 'your_password'
    #     }
    # }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# 允许所有的用户跨域请求
CORS_ORIGIN_ALLOW_ALL = True

# 指定自定义用户类
AUTH_USER_MODEL = 'users.User'

######################################### DEF的配置 #########################################
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 配置登录鉴权方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # 配置DRF使用的过滤器
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ),
    # 配置限流频率
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1/minute'
    }
}

######################################### token的相关配置 #########################################
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),  # 访问令牌的有效时间
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 刷新令牌的有效时间

    "ROTATE_REFRESH_TOKENS": False,  # 若为True, 则刷新后新的refresh_token有更新的有效时间
    "BLACKLIST_AFTER_ROTATION": True,  # 若为True, 刷新后的token将添加到黑名单中

    "ALGORITHM": "HS256",  # 对称算法: HS256 HS384 HS512  非对称算法: RSA
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,  # if signing_key, verifying_key will be ignore.
    "AUDIENCE": None,
    "ISSUER": None,

    "AUTH_HEADER_TYPES": ("Bearer",),  # Authorization: Bearer <token>
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",  # if HTTP_X_ACCESS_TOKEN, X_ACCESS_TOKEN: Bearer <token>
    "USER_ID_FIELD": "id",  # 使用唯一不变的数据库字段,将包含在生成的令牌中以标识用户
    "USER_ID_CLAIM": "user_id",
}

# 使用自定义的认证类进行身份认证(登录时验证用户信息)
AUTHENTICATION_BACKENDS = [
    'common.authenticate.MyBackend'
]

# 指定文件上传的路径
MEDIA_ROOT = BASE_DIR / 'file/image'
# 指定文件获取URL的路径
MEDIA_URL = 'file/image/'

######################################### celery配置 #########################################

# Broker配置, 使用Redis作为消息中间件
# CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
# Broker配置, 使用RabbitMQ作为消息中间件
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"

# BACKEND配置, 使用redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
# BACKEND配置, 使用RabbitMQ
# CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672/alarm"
# BACKEND配置, 使用django ORM
# CELERY_RESULT_BACKEND = 'django-db'
# 序列化方案
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'
# 任务过期时间
CELERY_RESULT_EXPIRES = 60 * 60 * 24
# 设置时区
CELERY_TIMEZONE = 'Asia/Shanghai'
# 设置定时任务
# CELERY_BEAT_SCHEDULER = {
#     'send-order-status-every-day': {
#         'task': 'order.tasks.send_order_status',
#         'schedule': crontab(hour='8', minute='0'),  # 每天早上8点执行
#     },
# }
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_WORKER_CONNECTION_RETRY_ON_STARTUP = True
# 解决时区问题
CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False
# worker数
CELERY_WORKER_CONCURRENCY = 10

######################################### 发送邮件配置配置 #########################################
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465  # 端口号
EMAIL_HOST_USER = '1256040887@qq.com'
EMAIL_HOST_PASSWORD = 'penjyorbigqxjieg'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_USE_SSL = True  # SSL加密
# EMAIL_USE_TLS = False  # TLS加密
