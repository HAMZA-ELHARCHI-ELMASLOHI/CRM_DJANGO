# CRM-DJANGO-REACT


- python -m venv venv
activate environment
- venv\Scripts\activate.bat

desactivate environment
- deactivate

- pip freeze > requirements.txt

start django project
- django-admin startproject  .
    

docker-compose up

docker-compose up -d --build

docker-compose down

docker exec -it d8bde4950075 python manage.py migrate

docker exec -it d8bde4950075 python manage.py createsuperuser

# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

#CMD gunicorn Django-CRM.wsgi.application --bind 0.0.0.0:$PORT
heroku container:login 
heroku container:push -a radiant-lake-93774 web  
heroku container:release -a radiant-lake-93774 web
heroku logs --tail -a radiant-lake-93774
heroku open -a=radiant-lake-93774

heroku run python manage.py makemigrations
heroku config:set DEBUG_COLLECTSTATIC=1

git:remote -a radiant-lake-93774

DEBUG=True
SECRET_KEY='t8ptgan4x64w+fscptls=nim-w70)ejqt6yue31nrh6l&r1o7j'
NAME=DJANGO_CRM
USER=postgres
HOST=localhost
PASSWORD=admin
PORT=5432




from pathlib import Path
import os
#import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.

'''
env=environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()
'''
DEBUG=True
#SECRET_KEY=os.environ.get('SECRET_KEY')

SECRET_KEY='fcsdfsd'
#DEBUG=env('DEBUG')
#SECRET_KEY=env('SECRET_KEY')
#DEBUG=os.environ.get('DEBUG')

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production


#ALLOWED_HOSTS = os.environ.get(list('ALLOWED_HOSTS'))

#ALLOWED_HOSTS=['127.0.0.1','radiant-lake-93774.herokuapp.com']
ALLOWED_HOSTS=['*']
# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'Dashboard.apps.DashboardConfig',
    'shop.apps.ShopConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters',
    "whitenoise.runserver_nostatic",

    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "whitenoise.middleware.WhiteNoiseMiddleware",

]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



ROOT_URLCONF = 'Django-CRM.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Django-CRM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}

import dj_database_url

DATABASE_URL = os.environ.get("DATABASE_URL")
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500
)
DATABASES["default"].update(db_from_env)


'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST':os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
    }
}
'''

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = "static_root"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL ='account.User'


LOGIN_REDIRECT_URL="/shop/products/"
SIGNUP_REDIRECT_URL="/shop/"

LOGOUT_REDIRECT_URL="/"

LOGIN_URL='/login'

APPEND_SLASH=False

#DEFAULT_AUTO_FIELD = 'django.db.models.UUIDField'

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
'''
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST") 
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER") 
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD") 
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get("EMAIL_PORT") 
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

'''

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = True
# USE_X_FORWARDED_PORT = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# X_FRAME_OPTIONS = "DENY"
# CSRF_TRUSTED_ORIGINS=['radiant-lake-93774.herokuapp.com'] 
# ALLOWED_HOSTS=['radiant-lake-93774.herokuapp.com']

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.mailgun.org' #env("EMAIL_HOST") 
EMAIL_HOST_USER = 'postmaster@sandbox821d3aa4b6554e0794b392d04119495c.mailgun.org' #env("EMAIL_HOST_USER") 
EMAIL_HOST_PASSWORD = '114e8951bc8f178ced1d52ba71f271ed-8d821f0c-9cfb762d'  #env("EMAIL_HOST_PASSWORD") 
EMAIL_USE_TLS = True
EMAIL_PORT = 587 #env("EMAIL_PORT") 
DEFAULT_FROM_EMAIL = 'postmaster@sandbox821d3aa4b6554e0794b392d04119495c.mailgun.org'# env("DEFAULT_FROM_EMAIL")

